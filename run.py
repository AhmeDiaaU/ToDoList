from app import app

if __name__ == '__main__':
    app.run(debug=True)

# Task routes
@app.route('/add', methods=['POST'])
@app.route('/update/<int:todo_id>', methods=['PUT'])
@app.route('/delete/<int:todo_id>', methods=['DELETE'])
@app.route('/archive/<int:todo_id>', methods=['PUT'])
@app.route('/unarchive/<int:todo_id>', methods=['PUT'])

# Category routes
@app.route('/category/add', methods=['POST'])
@app.route('/categories', methods=['GET'])

# Auth routes
@app.route('/login/register', methods=['POST'])
@app.route('/login/', methods=['POST'])
@app.route('/login/logout', methods=['GET'])

# Page routes
@app.route('/')
@app.route('/archive')
@app.route('/dashboard')
@app.route('/about')
@app.route('/profile')

@app.errorhandler(404)
def not_found_error(error):
    return "404 Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error", 500

@app.errorhandler(403)
def forbidden_error(error):
    return "403 Forbidden", 403

