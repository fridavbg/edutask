describe('Adding a task to a video', () => {

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
    cy.get('.todo-item').then(($len) => {
      cy.get('form input[type=text]').should('have.value', '');
      cy.get('input[placeholder="Add a new todo item"]').type(text, { force: true })
      cy.get('.inline-form').submit()
      cy.get('.todo-item:last').should('contain.text', text).then(() => {
        cy.get('.todo-item').then(($addedTask) => {
          // Check that task list is 1 value bigger than original task list
          expect($addedTask).to.have.length($len.length + 1)
        })
      })
    })
  })

  // Test case #2: The “Add” button remains disabled when description is empty so list length doesn't increase when pressing the button
  it('Test to press add button when description is empty', () => {
    cy.get('.todo-item').then(($len) => {
      cy.get('input[placeholder="Add a new todo item"]').clear({ force: true })
      cy.get('form input[type=text]').should('have.value', '');
      cy.get('.inline-form').submit()
      cy.get('.todo-item:last').should('contain.text', '').then(() => {
        cy.get('.todo-item').then(($addedTask) => {
          // Check that task list is is the same length as before pressing the Add button
          expect($addedTask).to.have.length($len.length)
        })
      })
    })
  })

  after(function () {
    cy.request('GET', `http://localhost:5000/users/bymail/${email}`).then((user) => {
      cy.request('DELETE', `http://localhost:5000/users/${user.body._id.$oid}`)
    }).then((response) => {
      cy.log(response.body)
    })
  })
})