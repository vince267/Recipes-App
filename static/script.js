let thing = document.querySelector('h1');
var colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'olive', 'pink', 'tan'];
var i = 0;
thing.addEventListener('click', function()
{
    thing.style.color = colors[i];
    i=(i+1)%(colors.length);
});


// The following functions are similar to the one found on https://digitalfox-tutorials.com/tutorial.php?title=How-to-add-remove-input-fields-dynamically-using-javascript
let form = document.forms[0];
function addIngredient(plusElement){

    let displayButton = document.querySelector(".stepheader");

    // Stopping the function if the three input fields have no value.
    if(plusElement.previousElementSibling.value.trim() === ""){
        return false;
    }
    if(plusElement.previousElementSibling.previousElementSibling.value.trim() === ""){
        return false;
    }
    if(plusElement.previousElementSibling.previousElementSibling.previousElementSibling.value.trim() === ""){
        return false;
    }

    // creating the div container.
    let div = document.createElement("div");
    div.setAttribute("class", "field");

    // Creating the input element.
    let field = document.createElement("input");
    field.setAttribute("type", "text");
    field.setAttribute("name", "ingredients[]");
    field.setAttribute("placeholder", "Ingredient");
    field.setAttribute("required", "");

    // Creating the input element.
    let field2 = document.createElement("input");
    field2.setAttribute("type", "number");
    field2.setAttribute("name", "amounts[]");
    field2.setAttribute("min", "0");
    field2.setAttribute("placeholder", "Amount");
    field2.setAttribute("required", "");



    // Creating the input element.
    let field3 = document.createElement("input");
    field3.setAttribute("type", "text");
    field3.setAttribute("name", "units[]");
    field3.setAttribute("placeholder", "Unit");
    field3.setAttribute("required", "");



    // Creating the plus span element.
    let plus = document.createElement("span");
    plus.setAttribute("onclick", "addIngredient(this)");
    let plusText = document.createTextNode("+");
    plus.appendChild(plusText);

    // Creating the minus span element.
    let minus = document.createElement("span");
    minus.setAttribute("onclick", "removeField(this)");
    let minusText = document.createTextNode("-");
    minus.appendChild(minusText);

    // Adding the elements to the DOM.
    form.insertBefore(div, displayButton);
    div.appendChild(field);
    div.appendChild(field2);
    div.appendChild(field3);
    div.appendChild(plus);
    div.appendChild(minus);

    // Un hiding the minus sign.
    plusElement.nextElementSibling.style.display = "block"; // the minus sign
    // Hiding the plus sign.
    plusElement.style.display = "none"; // the plus sign
}



function addStep(plusElement){

    let displayButton = document.querySelector(".stepheader2");

    // Stopping the function if the input field has no value.
    if(plusElement.previousElementSibling.value.trim() === ""){
        return false;
    }

    // creating the div container.
    let div = document.createElement("div");
    div.setAttribute("class", "field");

    // Creating the input element.
    let field = document.createElement("input");
    field.setAttribute("type", "text");
    field.setAttribute("name", "steps[]");
    field.setAttribute("placeholder", "Step");
    field.setAttribute("required", "");



    // Creating the plus span element.
    let plus = document.createElement("span");
    plus.setAttribute("onclick", "addStep(this)");
    let plusText = document.createTextNode("+");
    plus.appendChild(plusText);

    // Creating the minus span element.
    let minus = document.createElement("span");
    minus.setAttribute("onclick", "removeField(this)");
    let minusText = document.createTextNode("-");
    minus.appendChild(minusText);

    // Adding the elements to the DOM.
    form.insertBefore(div, displayButton);
    div.appendChild(field);
    div.appendChild(plus);
    div.appendChild(minus);

    // Un hiding the minus sign.
    plusElement.nextElementSibling.style.display = "block"; // the minus sign
    // Hiding the plus sign.
    plusElement.style.display = "none"; // the plus sign
}

function removeField(minusElement){
    minusElement.parentElement.remove();
}

