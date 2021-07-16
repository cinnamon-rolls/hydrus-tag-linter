import React from "react";
import AnchorButton from "./anchorButton";
import { getServerInfo } from "./apiHelper";
import Loading from "./loading";

class PageHome extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    if (this.state.summary == null) {
      this.refreshSummary();
    }
  }

  getSummary() {
    return this.state.summary;
  }

  async refreshSummary() {
    var serverInfo = await getServerInfo();
    var summary = [
      {
        name: "Hydrus API",
        value: [
          { name: "Version", value: serverInfo.hydrus_api_version },
          { name: "URL", value: serverInfo.hydrus_api_url },
        ],
      },
      {
        name: "Internal",
        value: [
          {
            name: "NODE_ENV",
            value: process.env.NODE_ENV,
          },
        ],
      },
    ];
    this.setState({ summary });
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

  renderRuleFileCount(ruleName) {
    var info = this.props.appBinds.getRuleInfo(ruleName);
    if (info == null) {
      return "?";
    }
    if (info.disabled === true) {
      return "Dsbld.";
    }

    var files = this.props.appBinds.getRuleFiles(ruleName);
    if (files == null) {
      return "?";
    }
    return <code>{files.length + ""}</code>;
  }

  renderRuleName(ruleName) {
    var info = this.props.appBinds.getRuleInfo(ruleName);
    var icon = null;

    if (info != null) {
      icon = info.icon;
    }

    return (
      <AnchorButton
        icon={icon}
        iconLeft="false"
        onClick={() => this.props.appBinds.viewRule(ruleName)}
        buttonText={ruleName}
      ></AnchorButton>
    );
  }

  renderRules() {
    var ruleNames = this.props.appBinds.getRuleNames();
    if (ruleNames == null) {
      return <Loading></Loading>;
    }
    if (ruleNames.length === 0) {
      return <p>No rules defined :(</p>;
    }
    return (
      <table>
        <thead>
          <tr>
            <th>Files</th>
            <th>Rule</th>
          </tr>
        </thead>
        <tbody>
          {ruleNames.map((ruleName) => (
            <tr key={ruleName + ".tr"}>
              <td style={{ textAlign: "right" }}>
                {this.renderRuleFileCount(ruleName)}
              </td>
              <td>{this.renderRuleName(ruleName)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
  /* {{ icon_span(text=rule.name, icon=rule.get_icon(), left=False) }} */

  renderSummary() {
    var summary = this.state.summary;
    if (summary == null) {
      return <Loading></Loading>;
    }
    return this.getSummary().map((section) =>
      this.renderSummarySectionTable(section)
    );
  }

  render() {
    return (
      <div>
        <h2>Rules</h2>
        {this.renderRules()}
        <h2>Summary</h2>
        {this.renderSummary()}
      </div>
    );
  }
}

export default PageHome;
