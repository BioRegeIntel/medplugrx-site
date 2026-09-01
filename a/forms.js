/* Submits Med Plug RX forms to /api/access and reports what actually happened.
   The previous handler cancelled the submit and painted a "Thank you" panel
   unconditionally, so a failure and a success looked identical to the person
   applying. Success is only shown here after the server accepts. */
(function () {
  function panel(title, body, tone) {
    return (
      '<div style="text-align:center;padding:60px 20px">' +
      '<div class="eyebrow">' + title + "</div>" +
      '<h3 class="serif" style="font-size:30px;font-weight:400;margin:18px 0">' +
      (tone === "error" ? "Not submitted" : "Thank you") +
      "</h3>" +
      '<p style="color:#A9A39A;max-width:460px;margin:0 auto;line-height:1.7">' +
      body +
      "</p></div>"
    );
  }

  document.querySelectorAll("form[data-endpoint]").forEach(function (form) {
    var stamp = Date.now();
    var btn = form.querySelector("button[type=submit], button:not([type])");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".formerr");
      if (note) note.remove();
      if (btn) {
        btn.disabled = true;
        btn.dataset.label = btn.textContent;
        btn.textContent = "Sending…";
      }

      var data = {};
      new FormData(form).forEach(function (v, k) {
        data[k] = v;
      });
      data.mp_ts = stamp;
      data.formType = form.dataset.formType || "application";

      fetch(form.dataset.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })
        .then(function (res) {
          return res.json().then(function (j) {
            return { ok: res.ok, body: j };
          });
        })
        .then(function (r) {
          if (r.ok && r.body && r.body.ok) {
            form.innerHTML = panel(
              "Received",
              form.dataset.successText ||
                "Our team will verify your licensure and respond within two business days."
            );
            return;
          }
          throw new Error(
            (r.body && r.body.error) ||
              "Something went wrong. Please email info@medplugrx.com directly."
          );
        })
        .catch(function (err) {
          if (btn) {
            btn.disabled = false;
            btn.textContent = btn.dataset.label || "Submit";
          }
          var p = document.createElement("p");
          p.className = "formerr";
          p.style.cssText =
            "color:#E0B4A6;font-size:13px;line-height:1.7;margin:16px 0 0;text-align:center";
          p.textContent = err.message;
          form.appendChild(p);
        });
    });
  });
})();
