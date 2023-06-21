from flask import Flask, request, render_template
import json

app = Flask(__name__)

def open_blog_storage():
    with open('storage.json', 'r') as data:
        blog_posts = json.load(data)
        return blog_posts

def edit_blog_storage(new_storage):
    with open('storage.json', 'w') as data:
        new_storage = json.dumps(new_storage)
        data.write(new_storage)

def unique_id():
    blog_posts = open_blog_storage()
    id_list = []
    for blog_post in blog_posts:
        id_list.append(blog_post['id'])
    for number in range(1000000000):
        if number not in id_list:
            return number



def fetch_post_by_id(post_id):
    blog_posts = open_blog_storage()
    for index, post in enumerate(blog_posts):
        if post['id'] == post_id:
            return post

@app.route('/')
def home():
    blog_posts = open_blog_storage()
    return render_template('home.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        content = request.form['content']

        blog_posts = open_blog_storage()
        new_id = unique_id()
        new_post = {"id": new_id, "author": name, "title": title, "content": content}
        blog_posts.append(new_post)
        edit_blog_storage(blog_posts)
        return home()
    else:
        return render_template('addform.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = open_blog_storage()
    for index, blog_post in enumerate(blog_posts):
        if post_id == blog_post['id']:
            del blog_posts[index]
    edit_blog_storage(blog_posts)
    return home()

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        content = request.form['content']

        blog_posts = open_blog_storage()
        for index, blog_post in enumerate(blog_posts):
            if post_id == blog_post['id']:
                del blog_posts[index]
        new_id = unique_id()
        new_post = {"id": new_id, "author": name, "title": title, "content": content}
        blog_posts.append(new_post)
        edit_blog_storage(blog_posts)
        return home()
    
    else:
        return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run()