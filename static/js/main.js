let item = {}

let ulElement = document.getElementById('list-container');

// make dropdown reflect selected item quantity
document.querySelectorAll('.dropdown-item').forEach(function(el) {
  el.addEventListener('click', function(event) {
    event.preventDefault();
    let parentDiv = event.target.closest('div.btn-group');
    parentDiv.querySelector('button.dropdown-toggle').innerText = this.innerHTML;
  });
});

ulElement.addEventListener('click', function(event) {
  let targetClasses = Array.from(event.target.classList);
  console.log(targetClasses)
   
  if(targetClasses.includes('dropdown-item')) {
    let itemInfo = event.target.closest('div.item-info');
    let itemName = itemInfo.querySelector('h2').innerText;
    let quantity = Number(event.target.innerText);
    let priceText = itemInfo.querySelector('.item-price').innerText;
    let parsedPrice = Number((priceText.replace(/[^0-9.-]+/g,"")));
    let priceCents = parsedPrice * 100; 
    item['itemName'] = itemName;
    item['quantity'] = quantity;
    item['priceCents'] = priceCents;
    item['price'] = priceText;
  }
});

let buttonGroup = document.querySelectorAll('.btn-group');
buttonGroup = Array.from(buttonGroup);
buttonGroup.forEach((button) => {
    button.addEventListener('click', function(e) {
    e.preventDefault();
  })
})

function search() {
  let searchQuery = document.getElementById('search-box').value;
  let searchResultContainer = document.getElementById('search-result-container')
  axios.get('/search/', { params: { 'query': searchQuery } }).then(function(response) {
    searchResultContainer.innerHTML = null;
    let title = document.createElement('h1');
    if(response.data.url) {
       title.innerText = `OUT OF STOCK: ${searchQuery}`
       searchResultContainer.appendChild(title);
       let image = document.createElement('img');
       image.src = response.data.url
       searchResultContainer.appendChild(image)
    }
    if(response.data.name) {
      title.innerText = response.data.name;
      searchResultContainer.appendChild(title);
      let image = document.createElement('img');
      image.src = `../../static/media/${response.data.filename}`;
      searchResultContainer.appendChild(image)
      let description = document.createElement('p');
      description.innerText = response.data.description;
      searchResultContainer.appendChild(description) 

      let price = document.createElement('div')
      price.innerText = response.data.price;
      searchResultContainer.appendChild(price)
    } 
  })
}

function addToCart() {
    axios.post('/cart/', item  ).then(function(response) {
      window.location.href = '/cart/'
    });
}

