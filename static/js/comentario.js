document.addEventListener("DOMContentLoaded", function() {
    let comments = document.querySelectorAll(".comment");
    let showMoreButton = document.getElementById("toggle-button");
    let showLessButton = document.getElementById("show-less-button");
    let visibleCount = 3;

    function updateCommentsVisibility() {
        comments.forEach((comment, index) => {
            comment.style.display = index < visibleCount ? "block" : "none";
        });

        if (visibleCount >= comments.length) {
            showMoreButton.style.display = "none";
            showLessButton.style.display = "none";
        } else {
            showMoreButton.style.display = "block";
            showLessButton.style.display = visibleCount > 3 ? "block" : "none";
        }
    }
    
    updateCommentsVisibility();
    
    showMoreButton.addEventListener("click", function() {
        visibleCount += 3;
        updateCommentsVisibility();
    });

    showLessButton.addEventListener("click", function() {
        if (visibleCount > 3) {
            visibleCount -= 3;
        }
        updateCommentsVisibility();
    });
});
