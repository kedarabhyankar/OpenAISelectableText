/**
 * @author Kedar Abhyankar
 * @email krabhyankar@gmail.com
 */

/**
 * This function is used to get the currently selected text on the page. It is invoked whenever the current selection
 * changes. This is monitored by an event listener defined later in this file.
 */
function getCurrentlySelectedText() {
    //Check if there's selected text already. If there is, set the text variable to this selected text. If not, then
    //once a range is created, select that new range as the text string
    let text = document.getSelection ?
        document.getSelection().toString() : document.selection.createRange().toString();
    //Set the inner html of the selected_text paragraph element so that the user knows what they have selected.
    document.getElementById('selected_text').innerHTML =
        "<p>" + text + "</p>";
    //Set the hidden field with the same text - this prevents having to go back and forth between Flask and JS, so
    //we store the result in the hidden field.
    document.getElementById('input_seltext').value = text;
}

/**
 * This is an event listener. Whenever an event, in this case, a selection change, occurs, the function below will be
 * invoked. In this case, it'll invoke the above getCurrentlySelectedText() function.
 */
document.addEventListener("selectionchange", () => {
    getCurrentlySelectedText()
});