import React, { PropTypes, Component } from 'react'
import Relay from 'react-relay'

class EventItem extends Component {
  constructor (props) {
    super(props)
    this.state = {}
  }
  static propTypes = {
    tagName: PropTypes.object
  }
  static defaultProps = {
    tagName: div
  }
  render () {
    {tagName} = this.props
    return (
      <{tagName} className="event-item">
        Stuff
      </{tagName}>
    )
  }
}

export default Relay.createContainer(EventItem, {
  fragments: {
    event: () => Relay.Ql`
      fragment on RoundEventNode {
        uuid
        trigger_label
      }
    `
  }
})
