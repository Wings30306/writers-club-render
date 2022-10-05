// Initialize Quill editor 

var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  ['blockquote'],

  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'header': [1, 2, 3, false] }],

  [{ 'align': [] }],

  ['clean']                                         // remove formatting button
];

let quill = new Quill('#editor', {
  theme: 'snow',
  modules: {
    toolbar: toolbarOptions
  }
});


// Variables
const form = document.querySelector('#form');
const editor = document.querySelector('#editor');
const hiddenInput = document.querySelector('#hidden-input');
const qlEditor = document.querySelector(".ql-editor");

// Listen for submit and intersept
form.addEventListener('submit', (event) => {
  
  // prevent form from being submitted until we are ready
  event.preventDefault();
  
  // get innerHTML from editor and convert to JSON
  let data = JSON.stringify(qlEditor.innerHTML);

  // apply json data to hidden input value
  if (data === "<p><br></p>"){
    hiddenInput.value = null;}
    else {
    hiddenInput.value = data;
    console.log(data)
  }
  

  // allow form to be submitted
  form.submit()
});