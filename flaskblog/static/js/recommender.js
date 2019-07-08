const API_URL = window.location.origin;

(() => {
  const form = document.getElementById('recommendationForm');
  form.onsubmit = (event) => {
    event.preventDefault();
    const genre = document.getElementById('genre').value; // Menjamo ID !!!

    console.log("Ime zanra je: " + genre)

    fetch(`${API_URL}/recommendations?genre=${genre}`)
      .then(response => {
        if (!response.ok) { throw response; }
        return response.json()
      })
      .then(data => {
        const filmList= document.getElementById('filmList');
        console.log("Pa nesto sam im rekao " + filmList)
        filmList.innerHTML = '';

        data.books.forEach(book => {
          //console.log(book)
          const bookItem = document.createElement('li');
          bookItem.appendChild(document.createTextNode(`${book}`));
          filmList.appendChild(bookItem);
        });
      })
      .catch(response => response.json().then(error => alert(error.message) ));
  }
})();
