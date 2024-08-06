from flask import Flask, render_template, request, flash
from openai import OpenAI

# @author Kedar Abhyankar, krabhyankar@gmail.com

app = Flask(__name__)
# A randomly generated UUID for the flash library to use.
app.secret_key = "c9587cd0-dbc9-4da2-86af-19f1516c08c7"
app.template_folder = "../templates"
app.static_folder = "../static"
# Define the OpenAI client
client = OpenAI()


# The default first page that opens; renders the home.html page
@app.route('/')
def pre_upload_home():
    return render_template('home.html')


# The page that we go to when we upload a file.
@app.route('/upload', methods=["POST"])
def post_upload_home():
    # The user should only be able to access this page from a POST request.
    if request.method == 'POST':
        f = request.files['file']
        # We suppress the following check (within PyCharm) so that more extensions can be handled in the future.
        # noinspection PyRedundantParentheses
        valid_extensions = ('.txt')
        # Check to see if the file is of .txt extension - or any of the other extensions
        # should any be added in the future.
        if not f.filename.endswith(valid_extensions):
            # If not, print an error and send it to flash so it can be displayed to the user.
            print('Invalid File Format. Expected one of [' + ''.join(valid_extensions + '].'))
            flash("You've uploaded a file that didn't match the correct format. "
                  "Valid extensions are [" + ''.join(valid_extensions) + "]. Please try again.")
            # Re-render the home page so the user can attempt to upload a new file again.
            return render_template('home.html')
        # Save the file under the static folder.
        f.save('tmp/' + f.filename)
        # Rewind the file pointer to the start - it shouldn't be changed prior to this, but it doesn't hurt.
        f.seek(0)
        # Read the content of the file.
        file_content = f.read()
        # The content is initially read as a bytes-like string, so we want to parse it to a utf-8 string for usability.
        file_content = file_content.decode('utf-8')
        # We want to preserve the format of the file, so we want to "remove" all new lines just like how it was in the
        # original file; this is because when we read in the file, it'll convert the new lines into \n as that is the
        # byte format. We want to undo that before passing it back to the frontend.
        file_content = file_content.split('\n')
        # Re-render the home page with the file_content field filled.
        return render_template('home.html', file_text=file_content)


@app.route('/process', methods=["POST"])
def process_gpt_4_output():
    # Get the value of the hidden field, called selected_text, which represents the text that the user has highlighted.
    selected_text = request.form.get('selected_text')
    # Invoke the GPT4 library using the "define" keyword as well as the user's selected text.
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "Define " + selected_text
            }
        ]
    )
    # Check to see if the response was completed. This can usually take some time (a few seconds).
    if completion:
        # If it's completed successfully, then print to the python console for good measure, set the response
        # variable to just the content of the response.
        print(completion.choices[0].message)
        response = completion.choices[0].message
    else:
        # On the off chance that it couldn't process the response, we will just say "Couldn't process" and the user
        # will have to try again.
        print("Couldn't process...")
        response = "Couldn't process..."

    # Re-render the home page with the openAI result present.
    return render_template("home.html", openai_result=response.content)


# The main invokes and starts up the flask project.
if __name__ == '__main__':
    app.run()
