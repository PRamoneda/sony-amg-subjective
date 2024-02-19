from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

@app.route('/compare/<path:algo0>/<path:algo1>/<path:algo2>', methods=['GET', 'POST'])
def compare_two(algo0, algo1, algo2):
    # adjust if required
    if request.method == 'POST':
        choice = request.form.get('election')
        print(f"Feedback received: {choice}")
        return redirect(url_for('compare_two', algo1=algo1, algo2=algo2))

    return render_template('compare.html',
                           experiment0_sample=algo0,
                           experiment1_sample=algo1,
                           experiment2_sample=algo2)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(debug=True)
