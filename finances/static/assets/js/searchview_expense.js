const search = document.getElementById("search")
const paginators = document.querySelector(".paginators")
const filler = document.querySelector("#tbodyonsearch")
const tbody = document.querySelector("#tbody")
const noresults = document.querySelector(".no-results")

search.addEventListener("keyup", (e) => {
    const searchVal = e.target.value;
    filler.innerHTML = "";

    if (searchVal.length > 0) {
        paginators.style.display = "none"
        fetch("search", {
            body: JSON.stringify({ "query": searchVal }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            tbody.style.display = "none";
            filler.style.display = "table-row-group;";
            if (data.length > 0) {
                noresults.style.display = "none";
                var count = 0;
                data.forEach(expense => {
                    count = count + 1;
                    var row = `
                    <tr>
                        <th scope="row">${count}</th>
                        <td>${expense.amount}</td>
                        <td>${expense.description}</td>
                        <td>${expense.date}</td>
                        <td>${expense.category}</td>
                        <td>${expense.file}</td>
                        <td style="text-align: center;">
                            <a class="btn btn-primary" href="{% url 'expense-edit' expense.id  %}">Update</a>
                        </td>
                    </tr>`;
                    filler.innerHTML += row;
                });
            }
            else {
                noresults.style.display = "block";
                tbody.style.display = "none";
                paginators.style.display = "none";
            }
        });
    }
    else {
        tbody.style.display = "table-row-group";
        noresults.display = "none";
        paginators.style.display = "block";
    }

});