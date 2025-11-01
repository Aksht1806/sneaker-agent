document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("image");
  const file = fileInput.files[0];
  const resultDiv = document.getElementById("result");
  const previewDiv = document.getElementById("preview");

  if (!file) {
    alert("Please upload an image first!");
    return;
  }

  // Preview image
  const reader = new FileReader();
  reader.onload = (event) => {
    previewDiv.innerHTML = `<img src="${event.target.result}" alt="Sneaker preview" />`;
  };
  reader.readAsDataURL(file);

  resultDiv.innerHTML = "Identifying sneaker... 👟";

  const formData = new FormData();
  formData.append("image", file);

  try {
    const response = await fetch("https://sneaker-agent.onrender.com/api/identify", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      resultDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
      return;
    }

    resultDiv.innerHTML = `
      <div class="result-card">
        <h2>${data.name || "Unknown Sneaker"}</h2>
        <p><b>Brand:</b> ${data.brand || "N/A"}</p>
        <p><b>Style Code:</b> ${data.style_code || "N/A"}</p>
      </div>
    `;
  } catch (error) {
    resultDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
});
