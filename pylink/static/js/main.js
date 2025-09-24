document.querySelectorAll(".copy-link").forEach(copyLinkContainer => {
	const inputField = copyLinkContainer.querySelector(".copy-link-input");
	const copyButton = copyLinkContainer.querySelector(".copy-link-button");

	inputField.addEventListener("focus", () => inputField.select());
	copyButton.addEventListener("click", () => {
		const text = inputField.value;

		inputField.select();
		navigator.clipboard.writeText(text);

		inputField.value = "Copied!";
		setTimeout(() => inputField.value = text, 2000)
	})
});

document.querySelectorAll(".copy-short-link").forEach(copyLinkContainer => {
	const inputField = copyLinkContainer.querySelector(".copy-short-link-input");
	const copyButton = copyLinkContainer.querySelector(".copy-short-link-button");

	inputField.addEventListener("focus", () => inputField.select());
	copyButton.addEventListener("click", () => {
		const text = inputField.value;

		inputField.select();
		navigator.clipboard.writeText(text);
	})
});

// 

document.querySelectorAll(".link-edit").forEach(element => {
	element.addEventListener("click", function(event){
		event.preventDefault();
		var linkId = this.getAttribute("link-id");

		var input = document.getElementById("link-input-name-" + linkId);

		div_input_impostor = document.getElementById("link-name-" + linkId)
		div_input_impostor.style.display = "none";

		input.style.display = "flex";
		input.classList.remove('d-none');

	})
});


// document.querySelectorAll(".qr-show").forEach(element => {
// 	element.addEventListener("click", function(event){
// 		event.preventDefault();
// 		var qrId = this.getAttribute("qr-id");
// 		var qrStatus = this.getAttribute("qr-status-" + qrId);

// 		var div = document.getElementById("qr-div-name-" + qrId);

// 		if(qrStatus == "none"){
// 			console.log(qrStatus.getAttribute("qr-status"));
// 			div.style.display = "flex";
// 			div.classList.remove('d-none');
// 			qrStatus.setAttribute("qr-status", "display");
// 		} else {
// 			console.log(qrStatus.getAttribute("qr-status"));
// 			div.style.display = "none";
// 			qrStatus.setAttribute("qr-status", "none");
// 		}
// 	})
// });

document.querySelectorAll(".qr-show").forEach(element => {
  element.addEventListener("click", function(event){
    event.preventDefault();
    event.stopPropagation();
    var qrId = this.getAttribute("qr-id");
    var div = document.getElementById("qr-div-name-" + qrId);

    if(div.style.display === "none" || div.classList.contains("d-none")){
      div.style.display = "flex";
      div.classList.remove("d-none");
    } else {
      div.style.display = "none";
    }
  });
});

async function downloadAs(type, filename, quality=0.92) {
  const img = document.getElementById('src');
  await img.decode();                    // ensure loaded

  const canvas = document.createElement('canvas');
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);

  // Use toBlob -> create object URL -> trigger download
  canvas.toBlob(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }, type, quality);
}

document.querySelectorAll('button[data-type]').forEach(btn => {
  btn.addEventListener('click', () => {
    const type = btn.getAttribute('data-type');
    const ext  = { "image/png":"png", "image/jpeg":"jpg", "image/webp":"webp" }[type];
    downloadAs(type, `my_qr.${ext}`, type === "image/jpeg" ? 0.9 : undefined);
  });
});