function requestVideo() {
    const credentials = getCredentials();

    const authorization = `Basic ${btoa(`${credentials.username}:${credentials.password}`)}`;
    const target = `${credentials.endpoint}/download?url=${credentials.url}`;

    fetch(target, {
        method: "GET",
        headers: {
            "Authorization": authorization
        }
    })
        .then(response => response.json())
        .then(json => {
            const textarea = $("#textarea_field");
            textarea.val(JSON.stringify(json));

            $("#download-section").show();

            setTimeout(enableDownloadButton, 10000);
        });
}

function enableDownloadButton() {
  $("#download-button").prop('disabled', false);
}

function downloadVideo() {
    const id = JSON.parse($("#textarea_field").val()).id;

    const credentials = getCredentials();
    const target = `${credentials.endpoint}/download/${id}?c=${btoa(`${credentials.username}:${credentials.password}`)}`;

    window.open(target);
}

function getCredentials() {
  const endpoint = $("#endpoint").val();
  const url = $("#url").val();
  const username = $("#username").val();
  const password = $("#password").val();

  return {
    endpoint: endpoint,
    url: url,
    username: username,
    password: password
  }
}