import React from 'react'
// import Relay from 'react-relay';

export default class Sumtin extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      name: props.name || 'Dave',
      thing_did: true
    }
  }
  render () {
    let {thing_did, name} = this.state
    return (<div>
      <h2>{thing_did ? 'did thing' : 'didn\'t do the thing'}</h2>
      <h1>Hello {name}</h1>
    </div>)
  }
}
