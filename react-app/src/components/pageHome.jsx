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

  getInternalSummary() {
    return {
      name: "Internal",
      value: [
        {
          name: "NODE_ENV",
          value: process.env.NODE_ENV,
        },
      ],
    };
  }

  renderSummarySectionTable(section) {
    return (
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
    );
  }

  renderRules() {
    return (
      <table>
        <thead>
          <tr>
            <th>Files</th>
            <th>Rule</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>ya</td>
            <td>aaa</td>
          </tr>
        </tbody>
      </table>
    );
  }

  render() {
    return (
      <div>
        <h2>Rules</h2>
        {this.renderRules()}
        <h2>Summary</h2>
        {this.getSummary().map((section) =>
          this.renderSummarySectionTable(section)
        )}
        {this.renderSummarySectionTable(this.getInternalSummary())}
      </div>
    );
  }
}

export default PageHome;
