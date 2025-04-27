document.addEventListener("DOMContentLoaded", function () {
    const comments = document.querySelectorAll(".comment");
    const showMoreButton = document.getElementById("toggle-button");
    const showLessButton = document.getElementById("show-less-button");
    let visibleCount = 6;

    function updateCommentsVisibility() {
        comments.forEach((comment, index) => {
            comment.style.display = index < visibleCount ? "flex" : "none";
        });

        if (showMoreButton) {
            showMoreButton.style.display = visibleCount >= comments.length ? "none" : "inline-block";
        }
        if (showLessButton) {
            showLessButton.style.display = visibleCount > 6 ? "inline-block" : "none";
        }
    }

    updateCommentsVisibility();

    if (showMoreButton) {
        showMoreButton.addEventListener("click", function () {
            visibleCount += 6;
            updateCommentsVisibility();
        });
    }

    if (showLessButton) {
        showLessButton.addEventListener("click", function () {
            visibleCount = Math.max(6, visibleCount - 6);
            updateCommentsVisibility();
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('.comment-input textarea');
    const form = document.querySelector('.comment-input');

    textarea.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); 
            form.submit();          
        }
    });
});
