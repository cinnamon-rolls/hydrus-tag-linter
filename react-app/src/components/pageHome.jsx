import React from "react";
import { fetchJson } from "./apiHelper";

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
    return fetchJson("server/get_summary").then((summary) =>
      this.setState({ summary })
    );
  }

  render() {
    return (
      <div>
        <h2>Summary</h2>
        {this.getSummary().map((section) => (
          <React.Fragment key={section.name + ".fragment"}>
            <h3>{section.name}</h3>
            <table>
              <tbody>
                {section.value.map((data) => (
                  <tr key={data.name}>
                    <td>{data.name}</td>
                    <td>
                      <code>{data.value + ""}</code>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </React.Fragment>
        ))}
      </div>
    );
  }
}

export default PageHome;
