import React from "react";

class PageHome extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    this.refreshSummary();
  }

  getSummary() {
    return this.state.summary || [];
  }

  async refreshSummary() {
    return fetch("/api/server/get_summary")
      .then((resp) => resp.json())
      .then((summary) => this.setState({ summary }));
  }

  render() {
    return (
      <div>
        <h2>Summary</h2>
        {this.getSummary().map((section) => (
          <div>
            <h3>{section.name}</h3>
            <table>
              {section.value.map((data) => (
                <tr>
                  <td>{data.name}</td>
                  <td>
                    <code>{data.value + ""}</code>
                  </td>
                </tr>
              ))}
            </table>
          </div>
        ))}
      </div>
    );
  }
}

export default PageHome;
