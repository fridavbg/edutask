describe('login into the server', () => {

  let email = 'jane.doe@gmail.com'
  beforeEach(function () {

    // Creates a user with dummy data
    cy.request('POST', 'http://localhost:5000/populate')
    cy.visit('http://localhost:3000')
    cy.contains('div', 'Email Address').find('input').type('jane.doe@gmail.com')
    cy.get('form').submit()
    cy.get('a img:first').click()
  })

  // Test cases for R8UC1


  it('Checks if input is empty', () => {
    cy.get('form input[type=text]').should('have.value', '');
  })

  after(function () {
    cy.request('GET', `http://localhost:5000/users/bymail/${email}`).then((user) => {
      cy.request('DELETE', `http://localhost:5000/users/${user.body._id.$oid}`)
    }).then((response) => {
      cy.log(response.body)
    })
  })
})