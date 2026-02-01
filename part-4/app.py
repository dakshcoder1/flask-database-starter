"""
Part 4: REST API with Flask
===========================
Build a JSON API for database operations (used by frontend apps, mobile apps, etc.)

What You'll Learn:
- REST API concepts (GET, POST, PUT, DELETE)
- JSON responses with jsonify
- API error handling
- Status codes
- Testing APIs with curl or Postman

Prerequisites: Complete part-3 (SQLAlchemy)
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)


# =============================================================================
# MODELS
# =============================================================================

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def to_dict(self):  # Convert model to dictionary for JSON response
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'isbn': self.isbn,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'author':{
                "id":self.author_id,
                "name":self.author.name,
                "city":self.author.city
                }if self.author else None
            }

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    bio= db.Column(db.Text)
    city = db.Column(db.String(100))
    books = db.relationship("Book",backref="author",lazy=True)

    def to_dict(self):
        return{
            "id": self.id,
            "name":self.name,
            "bio":self.bio,
            "city":self.city,
            "books":[
                {"id":book.id,
                 "title":book.title,
                 "year":book.year,
                 }for book in self.books
                 ]
        }
# =============================================================================
# REST API ROUTES
# =============================================================================


# GET /api/books - Get all books
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({  # Return JSON response
        'success': True,
        'count': len(books),
        'books': [book.to_dict() for book in books]  # List comprehension to convert all
    })


# GET /api/authors - Get all authors
@app.route('/api/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify({  # Return JSON response
        'success': True,
        'count': len(authors),
        'authors': [author.to_dict() for author in authors]  # List comprehension to convert all
    })


# GET /api/books/<id> - Get single book
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({
            'success': False,
            'error': 'Book not found'
        }), 404  # Return 404 status code

    return jsonify({
        'success': True,
        'book': book.to_dict()
    })
# GET /api/authors/<id> - Get single book
@app.route('/api/authors/<int:id>', methods=['GET'])
def get_author(id):
    author = Author.query.get(id)

    if not author:
        return jsonify({
            'success': False,
            'error': 'Author not found'
        }), 404  # Return 404 status code

    return jsonify({
        'success': True,
        'author': author.to_dict()
    })


# POST /api/books - Create new book
@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()  # Get JSON data from request body

    # Validation
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    if not data.get ('title'):
        return jsonify({'success': False, 'error': 'Title  are required'}), 400

    # Check for duplicate ISBN
    if data.get('isbn'):
        existing = Book.query.filter_by(isbn=data['isbn']).first()
        if existing:
            return jsonify({'success': False, 'error': 'ISBN already exists'}), 400

    # Create book
    new_book = Book(
        title=data['title'],
        author_id=data['author_id'],
        year=data.get('year'),  # Optional field
        isbn=data.get('isbn')
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Book created successfully',
        'book': new_book.to_dict()
    }), 201  # 201 = Created

# POST /api/authors - Create new author
@app.route('/api/authors', methods=['POST'])
def create_author():
    data = request.get_json()  # Get JSON data from request body
    print(data)

    # Validation
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    if not data.get ('name'):
        return jsonify({'success': False, 'error': 'Name  are required'}), 400



    # Create book
    new_author = Author(
        name=data.get('name'),
        bio=data.get('bio'),
        city=data.get('city')
    )
 
    db.session.add(new_author)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Author created successfully',
        'author': new_author.to_dict()
    }), 201  # 201 = Created


# PUT /api/books/<id> - Update book
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404

    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Update fields if provided
    if 'title' in data:
        book.title = data['title']
    if 'author_id' in data:
        book.author_id = data['author_id']
    if 'year' in data:
        book.year = data['year']
    if 'isbn' in data:
        book.isbn = data['isbn']

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Book updated successfully',
        'book': book.to_dict()
    })
# PUT /api/books/<id> - Update book
@app.route('/api/authors/<int:id>', methods=['PUT'])
def update_author(id):
    author = Author.query.get(id)

    if not author:
        return jsonify({'success': False, 'error': 'Author not found'}), 404

    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Update fields if provided
    if 'name' in data:
        author.name = data['name']
    if 'bio' in data:
        author.bio = data['bio']
    if 'city' in data:
        author.city = data['city']
    
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Author updated successfully',
        'author': author.to_dict()
    })



# DELETE /api/books/<id> - Delete book
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Book Deleted successfully'
    })

# DELETE /api/authors/<id> - Delete book
@app.route('/api/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get(id)

    if not author:
        return jsonify({'success': False, 'error': 'Author not found'}), 404

    db.session.delete(author)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Author deleted successfully'
    })



# =============================================================================
# BONUS: Search and Filter
# =============================================================================

# GET /api/books/search?q=python&author=john
@app.route('/api/books/search', methods=['GET'])
def search_books():
    query = Book.query

    # Filter by title (partial match)
    title = request.args.get('q')  # Query parameter: ?q=python
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))  # Case-insensitive LIKE

    # Filter by author
    author = request.args.get('author')
    if author:
     query = query.join(Author).filter(Author.name.ilike(f'%{author}%'))

    # Filter by year
    year = request.args.get('year')
    if year:
        query = query.filter_by(year=int(year))

    books = query.all()

    return jsonify({
        'success': True,
        'count': len(books),
        'books': [book.to_dict() for book in books]
    })

@app.route('/api/authors/search', methods=['GET'])
def search_authors():
    query = Author.query

    # Filter by name (partial match)
    name = request.args.get('q')  # Query parameter: ?q=python
    if name:
        query = query.filter(Author.name.ilike(f'%{name}%'))  # Case-insensitive LIKE

    # Filter by bio
    bio = request.args.get('bio')
    if bio:
        query = query.filter(Author.bio.ilike(f'%{bio}%'))

    # Filter by city
    city = request.args.get('city')
    if city:
        query = query.filter(Author.city.ilike(f'%{city}%'))

    authors = query.all()

    return jsonify({
        'success': True,
        'count': len(authors),
        'authors': [author.to_dict() for author in authors]
    })


@app.route('/api/books-advanced', methods=['GET'])
def get_books_advanced():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    allowed_fields = {
        "id": Book.id,
        "title": Book.title,
        "year": Book.year,
        "created_at": Book.created_at
    }

    sort_column = allowed_fields.get(sort, Book.id)

    query = Book.query
    query = query.order_by(sort_column.desc() if order == 'desc' else sort_column.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "page": page,
        "per_page": per_page,
        "total_pages": pagination.pages,
        "total_books": pagination.total,
        "books": [book.to_dict() for book in pagination.items]
    })


# =============================================================================
# SIMPLE WEB PAGE FOR TESTING
# =============================================================================


# =========================
# ROUTES (ALL ROUTES HERE)
# =========================

@app.route('/')
def index():
    return jsonify({
        "success": True,
        "message": "REST API is running",
        "endpoints": {
            "books": "/api/books",
            "authors": "/api/authors"
        }
    })

'''
# Get all books
curl http://localhost:5000/api/books

# Create a book
curl -X POST http://localhost:5000/api/books \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Flask Web Development", "author": "Miguel Grinberg", "year": 2018}'

# Update a book
curl -X PUT http://localhost:5000/api/books/1 \\
  -H "Content-Type: application/json" \\
  -d '{"year": 2023}'

# Delete a book
curl -X DELETE http://localhost:5000/api/books/1
        </pre>
    </body>
    </html>
    '''


# =============================================================================
# INITIALIZE DATABASE WITH SAMPLE DATA
# =============================================================================

def init_db():
    with app.app_context():
        db.create_all()

        if Author.query.count() ==0 :
            a1=Author(
                name="Eric Matthes",
                bio="Author of Python Crash Course",
                city="USA"
            )
            
            a2=Author(
                name="Miguel Grinberg",
                bio="Flask expert and author",
                city="USA"
            )
            a3=Author(
                name="Robert C. Martin",
                bio="Clean code and author",
                city="USA"
            )

            db.session.add_all([a1, a2, a3])
            db.session.commit()



        if Book.query.count() == 0:
            sample_books = [
                Book(title='Python Crash Course', author_id=a1.id, year=2019, isbn='978-1593279288'),
                Book(title='Flask Web Development', author_id=a2.id, year=2018, isbn='978-1491991732'),
                Book(title='Clean Code', author_id=a3.id, year=2008, isbn='978-0132350884'),
            ]
            db.session.add_all(sample_books)
            db.session.commit()
            print('Sample books and authors added!')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)


# =============================================================================
# REST API CONCEPTS:
# =============================================================================
#
# HTTP Method | CRUD      | Typical Use
# ------------|-----------|---------------------------
# GET         | Read      | Retrieve data
# POST        | Create    | Create new resource
# PUT         | Update    | Update entire resource
# PATCH       | Update    | Update partial resource
# DELETE      | Delete    | Remove resource
#
# =============================================================================
# HTTP STATUS CODES:
# =============================================================================
#
# Code | Meaning
# -----|------------------
# 200  | OK (Success)
# 201  | Created
# 400  | Bad Request (client error)
# 404  | Not Found
# 500  | Internal Server Error
#
# =============================================================================
# KEY FUNCTIONS:
# =============================================================================
#
# jsonify()           - Convert Python dict to JSON response
# request.get_json()  - Get JSON data from request body
# request.args.get()  - Get query parameters (?key=value)
#
# =============================================================================


# =============================================================================
# EXERCISE:
# =============================================================================
#
# 1. Create new class say "Author" with fields id, name, bio, city with its table. 
# Write all CRUD api routes for it similar to Book class.
# Additionally try to link Book and Author class such that each book has one author and one author can have multiple books.

# 1. Create 2 simple frontend using JavaScript fetch()
# This is a bigger exercise. Create a frontend in HTML and JS that uses all api routes and displays data dynamically, along with create/edit/delete functionality.
# Since the API is through n through accessible on the computer/server, you don't need to use render_template from flask, instead, 
# you can directly use ipaddress:portnumber/apiroute from any where. So your HTML JS code can be anywhere on computer (not necessarily in flask)  

# 3. Add pagination: `/api/books?page=1&per_page=10` 
# Hint - the sqlalchemy provides paginate method. 
# OPTIONAL - For ease of understanding, create a new api say /api/books-with-pagination which takes page number and number of books per page

# 4. Add sorting: `/api/books?sort=title&order=desc`
# OPTIONAL - For ease of understanding, create a new api say /api/books-with-sorting
#
# =============================================================================
