describe('loggin into the server', () => {

  let uid
  let name
  beforeEach(function () {

    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response)=> {
          uid = response.body._id.$iod
          name = user.firstName + ' ' + user.lastName
        })
      })
  })

  beforeEach(function () {
    cy.visit('http://localhost:3000')
  })

  it('starting out on the landing screen', () => {
    cy.get('h1')
      .should('contain.text', 'Login')
  })

  it('email field enabled', () => {
    cy.get('.inputwrapper #email')
      .should('be.enabled')
  })
})