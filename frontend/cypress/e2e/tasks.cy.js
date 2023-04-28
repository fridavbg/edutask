describe('Test cases for requirement 8 of the EduTask specification', () => {

  let email = 'jane.doe@gmail.com'
  let text = 'Testing adding task'
  beforeEach(function () {

    // Creates a user with dummy data
    cy.request('POST', 'http://localhost:5000/populate')
    cy.visit('http://localhost:3000')
    cy.contains('div', 'Email Address').find('input').type('jane.doe@gmail.com')
    cy.get('form').submit()
    cy.get('a img:first').click()
  })

  // Test cases for R8UC1
  //
  // Test case #1: Create a new todo item when user presses "Add" and description is not empty
  it('Test to create a new todo item', () => {
    cy.get('.todo-item').its('length').then((len) => {
      cy.get('input[placeholder="Add a new todo item"]').type(text, { force: true });
      cy.get('.inline-form').submit();
      cy.get('.todo-item:last').should('contain.text', text);
      // Check how many todo items there are after adding a new one
      cy.get('.todo-item').its('length').should('eq', len + 1);
    });
  })

  // Test case #2: The “Add” button remains disabled when description is empty so list length doesn't increase when pressing the button
  it('Test to press Add button when description is empty', () => {
    cy.get('.todo-item').its('length').then((len) => {
      cy.get('input[placeholder="Add a new todo item"]').clear({ force: true });
      cy.get('.inline-form').submit();

      // Check that no new todo item is added
      cy.get('.todo-item:last').should('contain.text', '');
      cy.get('.todo-item').its('length').should('eq', len);
    });
  });

  // Test cases for R8UC2
  //
  // Test case #1: The active todo item is set to done
  it('Test to toggle the active todo item to done', () => {
    cy.get('.checker:first').click().then(() => {
      cy.get('ul').find('.todo-item:first').find('.checker').click({ force: true })
      cy.get('.todo-item:first .editable').should('have.css', 'text-decoration-line').and('eq', 'line-through');
    })
  })


  // Test case #2: The done todo item is set to active
  it('Test to toggle the done todo item to active', () => {
    cy.get('.checker:first').click().then(() => {
      cy.get('ul').find('.todo-item:first').find('.checker').click({ force: true })
      cy.get('ul').find('.todo-item:first').find('.checker').click({ force: true })
      cy.get('.todo-item:first .editable').should('not.have.css', 'text-decoration-line', 'line-through');
    })
  })

  // Test cases for R8UC3
  //
  // Test case #1: The todo task should be removed
  it('Test to remove the todo item', () => {
    cy.get('.todo-item').its('length').then((len) => {
      cy.get('.remover:first').click();
      cy.get('.todo-item').its('length').should('eq', len - 1);
    });
  })


  after(function () {
    cy.request('GET', `http://localhost:5000/users/bymail/${email}`).then((user) => {
      cy.request('DELETE', `http://localhost:5000/users/${user.body._id.$oid}`)
    }).then((response) => {
      cy.log(response.body)
    })
  })
})