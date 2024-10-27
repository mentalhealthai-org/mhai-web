// Function to get CSRF token from cookies
function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

export default getCSRFToken;
