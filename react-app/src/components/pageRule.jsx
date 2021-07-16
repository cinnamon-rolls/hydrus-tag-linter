import React from "react";
import Gallery from "./gallery";
import "./pageRule.css";

class PageRule extends React.Component {
  render() {
    var appBinds = this.props.appBinds;

    var ruleName = this.props.ruleName;
    var ruleInfo = appBinds.getRuleInfo(ruleName);
    var ruleFiles = appBinds.getRuleFiles(ruleName);
    var ruleFileCount = ruleFiles != null ? ruleFiles.length : "?";

    if (this.props.ruleName == null) {
      return <p>Rule not found :(</p>;
    }
    return (
      <React.Fragment>
        <div id="side_info">
          <h2>{ruleName}</h2>
          <p>{ruleInfo.note || "This rule does not have a note."}</p>
          <p>
            There are <code>{ruleFileCount}</code> files to review.
          </p>
        </div>

        <div id="all_galleries_container">
          <div id="noncompliance_gallery_container">
            <h2>Files</h2>
            <Gallery appBinds={appBinds} filesCallback={() => appBinds.getRuleFiles(ruleName)} />
          </div>

          <div id="exempt_gallery_container">
            <h2>Exemptions</h2>
            <Gallery />
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default PageRule;
