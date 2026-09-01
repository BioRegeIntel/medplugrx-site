// Physician account applications and professional referrals.
//
// This endpoint exists because the form on access.html never had one. Its
// submit handler called preventDefault(), replaced itself with a "Thank you"
// panel, and sent nothing anywhere — no action, no endpoint, and no name
// attribute on a single input. Every application since that page went live was
// discarded in the browser. Nothing here is clever; it just has to actually
// deliver, and fail loudly when it cannot.

const TO = ["info@medplugrx.com"];
const RESEND_KEY = process.env.RESEND_API_KEY;
const FROM = process.env.LEAD_FROM || "Med Plug RX <onboarding@resend.dev>";

// Best-effort burst control. Serverless instances are recycled, so this is a
// speed bump for casual abuse rather than a real rate limiter.
const buckets = new Map();
function rateLimit(key, limit, windowMs) {
  const now = Date.now();
  const b = buckets.get(key);
  if (!b || now > b.reset) {
    buckets.set(key, { n: 1, reset: now + windowMs });
    return true;
  }
  if (b.n >= limit) return false;
  b.n += 1;
  return true;
}

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const LABELS = {
  firstName: "First name",
  lastName: "Last name",
  practice: "Practice / facility",
  specialty: "Specialty",
  npi: "NPI",
  licenseState: "State of licensure",
  email: "Email",
  phone: "Phone",
  city: "City",
  interest: "Preparations of interest",
  referrerName: "Referred by — name",
  referrerOrganization: "Referred by — practice",
  referrerEmail: "Referred by — email",
  referralConsent: "Permission to share confirmed",
  noPhi: "No patient information confirmed",
};

// Field names we never want to receive. If a client ever starts sending these,
// the submission is refused rather than quietly emailed to an inbox.
const PROHIBITED = /^(patient|dob|dateofbirth|diagnosis|mrn|medicalrecord|insurance|treatment)/i;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  // Same-origin only. The form is the only intended caller.
  const origin = req.headers.origin || "";
  const host = req.headers.host || "";
  if (origin && !origin.endsWith(host)) {
    return res.status(403).json({ ok: false, error: "Bad origin" });
  }

  const ip =
    (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (!rateLimit(ip, 5, 10 * 60 * 1000)) {
    return res
      .status(429)
      .json({ ok: false, error: "Too many submissions. Please try again later." });
  }

  const data = typeof req.body === "object" && req.body ? req.body : {};

  // Honeypot: hidden fields no human fills in.
  if (data.mp_website || data.mp_company_url) {
    return res.status(202).json({ ok: true });
  }
  // Submitted faster than a person can type.
  if (data.mp_ts && Date.now() - Number(data.mp_ts) < 3000) {
    return res.status(202).json({ ok: true });
  }

  for (const k of Object.keys(data)) {
    if (PROHIBITED.test(k)) {
      return res.status(400).json({
        ok: false,
        error:
          "This form does not accept patient information. Please remove it and submit professional details only.",
      });
    }
  }

  const kind = data.formType === "referral" ? "referral" : "application";
  const required =
    kind === "referral"
      ? ["firstName", "lastName", "email", "referrerName", "referrerEmail"]
      : ["firstName", "lastName", "practice", "email", "licenseState"];
  const missing = required.filter((f) => !String(data[f] || "").trim());
  if (missing.length) {
    return res.status(422).json({ ok: false, error: "Missing required fields." });
  }

  const rows = Object.entries(data)
    .filter(([k, v]) => !k.startsWith("mp_") && k !== "formType" && String(v ?? "").trim())
    .map(
      ([k, v]) =>
        `<tr><td style="padding:5px 16px 5px 0;color:#5c6670;vertical-align:top">${esc(
          LABELS[k] || k
        )}</td><td style="padding:5px 0"><b>${esc(v)}</b></td></tr>`
    )
    .join("");

  const heading =
    kind === "referral"
      ? "New Med Plug RX professional referral"
      : "New Med Plug RX physician account application";
  const html = `<h2 style="font-family:Georgia,serif;color:#0a0908">${heading}</h2><table style="font-family:Arial,sans-serif;font-size:14px">${rows}</table>`;
  const subject = `${heading} — ${esc(data.firstName || "")} ${esc(
    data.lastName || ""
  )}`.trim();

  if (!RESEND_KEY) {
    // No mail credential configured. Say so instead of showing a success
    // panel — a silent thank-you is exactly the failure being fixed here.
    console.error("access: RESEND_API_KEY is not set; submission not delivered", subject);
    return res.status(503).json({
      ok: false,
      error:
        "We could not submit your application automatically. Please email info@medplugrx.com and we will respond within two business days.",
    });
  }

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${RESEND_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: FROM,
        to: TO,
        subject,
        html,
        ...(data.email ? { reply_to: String(data.email) } : {}),
      }),
    });
    if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
  } catch (err) {
    console.error("access: delivery failed", err);
    return res.status(502).json({
      ok: false,
      error:
        "We could not submit your application automatically. Please email info@medplugrx.com and we will respond within two business days.",
    });
  }

  return res.status(202).json({ ok: true });
}
