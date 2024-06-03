describe('Manipulating the todo list associated to a task', () => {
  let uid
  let name
  let email
  let taskid

  beforeEach(function () {
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          cy.log(response)
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      }).then(() => {
        cy.fixture('task.json').as('task')
          .then((task) => {
            task['userid'] = uid
          })
          .then((task) => {
            cy.request({
              method: 'POST',
              url: 'http://localhost:5000/tasks/create',
              form: true,
              body: task
            }).then((response) => {
              taskid = response.body[0]._id.$oid
            })
          })

        cy.visit('http://localhost:3000')

        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)

        cy.get('form')
          .submit()

        cy.get('h1')
          .should('contain.text', 'Your tasks, ' + name)

        cy.get('.container-element')
          .find('a')
          .click()

      })
  })

  it('User has not yet entered a description of a todo item into the form', () => {
    cy.get('.inline-form')
      .find('input[type=text]')
      .should('be.empty')

    cy.get('input[type=submit')
      .should('be.disabled')
  })

  it('User creates a new todo', () => {
    cy.get('.inline-form')
      .find('input[type=text]')
      .type('Todo description')

    cy.get('.inline-form')
      .submit()

    cy.get('.todo-item').last()
      .should('contain.text', 'Todo description')

    cy.get('.todo-item').last()
      .find('span').first()
      .should('have.class', 'checker unchecked')
  })

  it('User changes active todo to done', () => {
    cy.get('.todo-item')
      .find('span').first()
      .should('have.class', 'checker unchecked')

    cy.get('.todo-item')
      .find('span').first()
      .trigger('click')

    cy.get('.todo-item')
      .find('span').first()
      .should('have.class', 'checker checked')
  })

  it('User changes done todo to active', () => {
    cy.get('.todo-item')
      .find('span').first()
      .should('have.class', 'checker checked')

    cy.get('.todo-item')
      .find('span').first()
      .trigger('click')

    cy.get('.todo-item')
      .find('span').first()
      .should('have.class', 'checker unchecked')
  })

  it('User deletes a todo item', () => {
    cy.get('.todo-item')
      .should('contain.text', 'Todo description')
      .find('.remover').last()
      .trigger('click')

    cy.get('.todo-item')
      .should('not.contain.text', 'Todo description')
  })

  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})