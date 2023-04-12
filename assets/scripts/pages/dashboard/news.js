(async function () {
    const newsPanel = document.querySelector('#news-panel');
    if (!newsPanel) {
        return;
    }

    const loadMoreButton = document.querySelector('#news-load-button');
    const loadMoreSpinner = document.querySelector('#load-more-spinner');

    let page = 1;
    let newsCount = 0;

    await loadNextNews();
    endLoad();

    loadMoreButton.addEventListener('click', async () => {
        await loadNextNews();
        endLoad();
    });

    async function loadNextNews() {
        startLoad();

        const response = await fetch(Routing.generate('app_news_list', {page: page}));
        if (!response.status) {
            return;
        }

        const data = await response.json();
        if (data.length === 0) {
            loadMoreButton.setAttribute('disabled', 'disabled');
            loadMoreButton.setAttribute('no-more-news', true);
            loadMoreButton.innerText = 'No more news';

            return;
        }

        for (const postData of data) {
            const postTemplate = createPost(postData.title, postData.description);
            newsPanel.appendChild(postTemplate);
        }

        page += 1;
    }

    function createPost(title, description) {
        const template = document.createElement('template');
        template.innerHTML = `
            <div class="accordion-item">
                <h4 class="accordion-header" id="news-${newsCount}-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#news-${newsCount}-body" aria-expanded="false" aria-controls="news-${newsCount}-body">
                        ${title}
                    </button>
                </h4>
                <div id="news-${newsCount}-body" class="accordion-collapse collapse" aria-labelledby="news-${newsCount}-header">
                    <div class="accordion-body">
                        ${description}
                    </div>
                </div>
            </div>
        `.trim();

        newsCount += 1;

        return template.content.firstChild;
    }

    function startLoad() {
        loadMoreButton.setAttribute('disabled', 'disabled');
        loadMoreSpinner.classList.remove('d-none');
    }

    function endLoad() {
        loadMoreSpinner.classList.add('d-none');

        if (!loadMoreButton.getAttribute('no-more-news')) {
            loadMoreButton.removeAttribute('disabled');
        }
    }
})();