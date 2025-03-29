document.getElementById("searchForm").addEventListener("submit", function(e) {
    // Optional: Prevent form submission for client-side validation
    // e.preventDefault();
    console.log("Form submitted with city: " + document.querySelector("input[name='city']").value);
    
    // Add loading feedback
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Loading events...</p>";
});
