describe("Test cases for requirement 8 of the EduTask specification", () => {
    let email, userId;
    let todo = "new todo";

    before("create a dummy user", () => {
        cy.fixture("user.json").then((user) => {
            cy.request({
                method: "POST",
                url: "http://localhost:5000/users/create",
                form: true,
                body: user,
            }).then((response) => {
                userId = response.body._id.$oid;
                email = user.email;
            });
        });
    });

    before("create dummy tasks", () => {
        cy.fixture("tasks.json").then((task) => {
            task.userid = userId;
            cy.request({
                method: "POST",
                url: "http://localhost:5000/tasks/create",
                form: true,
                body: task,
            });
        });
    });

    beforeEach(function () {
        cy.visit("http://localhost:3000");
        cy.contains("div", "Email Address").find("input").type(email);
        cy.get("form").submit();
        cy.get("a img:first").click();
    });

    it("should create a todo", () => {
        cy.get("div.popup")
            .find("input[type=text]")
            // check that the input field is writeable and cleared
            .should("be.enabled")
            .type(todo, { force: true });
        cy.get("div.popup").find("input[type=submit]").click({ force: true });

        cy.contains("li", `${todo}`).should("exist");

        // Check if the new todo item has the same text as the todo variable
        cy.get(".todo-item:last").should("contain.text", todo);
    });

    it("should contain a disabled Add button", () => {
        cy.get("div.popup").find("input[type=submit]").should("be.disabled");
    });

    // Test cases for R8UC1
    //
    // Test case #1: Create a new todo item when user presses "Add" and description is not empty
    it("Test to create a new todo item", () => {
        cy.get(".todo-item")
            .its("length")
            .then((len) => {
                cy.get('input[placeholder="Add a new todo item"]').type(todo, {
                    force: true,
                });
                cy.get(".inline-form").submit();
                cy.get(".todo-item:last").should("contain.text", todo);
                // Check how many todo items there are after adding a new one
                cy.get(".todo-item")
                    .its("length")
                    .should("eq", len + 1);
            });
    });

    // Test case #2: The “Add” button remains disabled when description is empty so list length doesn't increase when pressing the button
    it("Test to press Add button when description is empty", () => {
        cy.get(".todo-item")
            .its("length")
            .then((len) => {
                cy.get('input[placeholder="Add a new todo item"]').clear({
                    force: true,
                });
                cy.get(".inline-form").submit();

                // Check that no new todo item is added
                cy.get(".todo-item:last").should("contain.text", "");
                cy.get(".todo-item").its("length").should("eq", len);
            });
    });

    // Test cases for R8UC2
    //
    // Test case #1: The active todo item is set to done
    it("Test to toggle the active todo item to done", () => {
        cy.get(".checker:first")
            .click()
            .then(() => {
                cy.get("ul")
                    .find(".todo-item:first")
                    .find(".checker")
                    .click({ force: true });
                cy.get(".todo-item:first .editable")
                    .should("have.css", "text-decoration-line")
                    .and("eq", "line-through");
            });
    });

    // Test case #2: The done todo item is set to active
    it("Test to toggle the done todo item to active", () => {
        cy.get(".checker:first")
            .click()
            .then(() => {
                cy.get("ul")
                    .find(".todo-item:first")
                    .find(".checker")
                    .click({ force: true });
                cy.get("ul")
                    .find(".todo-item:first")
                    .find(".checker")
                    .click({ force: true });
                cy.get(".todo-item:first .editable").should(
                    "not.have.css",
                    "text-decoration-line",
                    "line-through"
                );
            });
    });

    // Test cases for R8UC3
    //
    // Test case #1: The todo task should be removed
    it("Test to remove a todo item", () => {
        cy.get(".todo-item")
            .its("length")
            .then((len) => {
                cy.get(".remover:first").click({ force: true });
                cy.get(".todo-item")
                    .its("length")
                    .should("eq", len - 1);
            });
    });

    after(function () {
        cy.request("GET", `http://localhost:5000/users/bymail/${email}`)
            .then((user) => {
                cy.request(
                    "DELETE",
                    `http://localhost:5000/users/${user.body._id.$oid}`
                );
            })
            .then((response) => {
                cy.log(response.body);
            });
    });
});
