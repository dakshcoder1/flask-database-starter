const BOOK_API = "http://localhost:5000/api/books";
const AUTHORS_API = "http://localhost:5000/api/authors";

/* ================= BOOKS ================= */

const API = "http://127.0.0.1:5000/api/books";

/* 📚 Load Books */
function loadBooks() {
    fetch(API)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("bookList");
            if (!list) return;

            list.innerHTML = "";

            data.books.forEach(book => {
                list.innerHTML += `
                    <li>
                        <strong>${book.title}</strong><br>
                        Year: ${book.year || "N/A"}<br>
                        Author ID: ${book.author.id}<br>
                        ISBN: ${book.isbn || "N/A"}
                        <br><br>
                        <button onclick="deleteBook(${book.id})">🗑 Delete</button>
                        <button onclick='openEdit(${JSON.stringify(book)})'>✏️ Edit</button>
                    </li>
                `;
            });
        });
}

/* ➕ Add Book */
const bookForm = document.getElementById("bookForm");
if (bookForm) {
    bookForm.addEventListener("submit", function(e){
        e.preventDefault();

        const book = {
            title: title.value,
            author_id: author_id.value,
            year: year.value,
            isbn: isbn.value
        };

        fetch(API, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(book)
        })
        .then(() => {
            this.reset();
            loadBooks();
        });
    });
}

/* 🗑 Delete */
function deleteBook(id) {
    fetch(`${API}/${id}`, { method: "DELETE" })
        .then(() => loadBooks());
}

/* ✏️ OPEN EDIT FORM */
function openEdit(book) {
    document.getElementById("editBookCard").style.display = "block";

    edit_id.value = book.id;
    edit_title.value = book.title;
    edit_author_id.value = book.author.id;
    edit_year.value = book.year || "";
    edit_isbn.value = book.isbn || "";
}

/* ❌ CLOSE EDIT */
function closeEdit() {
    document.getElementById("editBookCard").style.display = "none";
}

/* ✅ UPDATE BOOK */
const editBookForm = document.getElementById("editBookForm");
if (editBookForm) {
    editBookForm.addEventListener("submit", function(e){
        e.preventDefault();

        const id = edit_id.value;

        const updatedBook = {
            title: edit_title.value,
            author_id: edit_author_id.value,
            year: edit_year.value,
            isbn: edit_isbn.value
        };

        fetch(`${API}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedBook)
        })
        .then(() => {
            closeEdit();
            loadBooks();
        });
    });
}

/* 🔍 Search */
function filterBooks() {
    const val = searchInput.value.toLowerCase();
    document.querySelectorAll("#bookList li").forEach(li => {
        li.style.display = li.textContent.toLowerCase().includes(val) ? "block" : "none";
    });
}


/* ================= AUTHORS ================= */

const AUTHOR_API = "http://localhost:5000/api/authors";

/* ================= LOAD AUTHORS ================= */
function loadAuthors() {
    fetch(AUTHOR_API)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("authorList");
            if (!list) return;

            list.innerHTML = "";

            data.authors.forEach(author => {
                list.innerHTML += `
                    <li>
                        <strong>${author.name}</strong><br>
                        Bio: ${author.bio || "N/A"}<br>
                        City: ${author.city || "N/A"}<br><br>
                        <button onclick="openEdit(${author.id})">✏️ Edit</button>
                        <button onclick="deleteAuthor(${author.id})">🗑 Delete</button>
                    </li>
                `;
            });
        })
        .catch(err => console.error("Error loading authors:", err));
}

/* ================= ADD AUTHOR ================= */
const authorForm = document.getElementById("authorForm");
if (authorForm) {
    authorForm.addEventListener("submit", e => {
        e.preventDefault();

        const author = {
            name: document.getElementById("name").value,
            bio: document.getElementById("bio").value,
            city: document.getElementById("city").value
        };

        fetch(AUTHOR_API, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(author)
        })
        .then(res => {
            if (!res.ok) return res.json().then(err => { throw err });
            return res.json();
        })
        .then(() => {
            authorForm.reset();
            loadAuthors();
        })
        .catch(err => alert(err.error || "Error adding author"));
    });
}

/* ================= DELETE AUTHOR ================= */
function deleteAuthor(id) {
    fetch(`${AUTHOR_API}/${id}`, { method: "DELETE" })
        .then(() => loadAuthors());
}

/* ================= OPEN EDIT FORM ================= */
function openEdit(id) {
    fetch(`${AUTHOR_API}/${id}`)
        .then(res => res.json())
        .then(data => {
            if (!data.author) return;

            const editCard = document.getElementById("editCard");
            editCard.style.display = "block";

            document.getElementById("edit_id").value = data.author.id;
            document.getElementById("edit_name").value = data.author.name;
            document.getElementById("edit_bio").value = data.author.bio || "";
            document.getElementById("edit_city").value = data.author.city || "";
        });
}

/* ================= CLOSE EDIT FORM ================= */
function closeEdit() {
    document.getElementById("editCard").style.display = "none";
}

/* ================= UPDATE AUTHOR ================= */
const editForm = document.getElementById("editForm");
if (editForm) {
    editForm.addEventListener("submit", e => {
        e.preventDefault();

        const id = document.getElementById("edit_id").value;

        const updatedAuthor = {
            name: document.getElementById("edit_name").value,
            bio: document.getElementById("edit_bio").value,
            city: document.getElementById("edit_city").value
        };

        fetch(`${AUTHOR_API}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedAuthor)
        })
        .then(() => {
            closeEdit();
            loadAuthors();
        });
    });
}

/* ================= SEARCH ================= */
function filterAuthors() {
    const searchInput = document.getElementById("searchInput");
    const value = searchInput.value.toLowerCase();
    document.querySelectorAll("#authorList li").forEach(li => {
        li.style.display = li.textContent.toLowerCase().includes(value)
            ? "block"
            : "none";
    });
}

/* ================= LOAD AUTHORS ON PAGE LOAD ================= */
document.addEventListener("DOMContentLoaded", () => {
    loadAuthors();
});
