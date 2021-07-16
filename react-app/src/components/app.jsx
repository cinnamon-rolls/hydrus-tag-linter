// import "./App.css";
import React from "react";
import Navigation from "./navigation";

import PageHome from "./pageHome";
import PageSearch from "./pageSearch";
import PageNotFound from "./pageNotFound";
import PageFile from "./pageFile";
import PageRule from "./pageRule";
import { getRuleNames, getRuleFiles, getRuleInfo } from "./apiHelper";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      page: "home",
      ruleInspected: null,
      ruleNames: [],
      ruleInfos: {},
      ruleFiles: {},
    };
  }

  componentDidMount() {
    this.refreshRuleNames();
  }

  async refreshRuleNames() {
    // var lastRuleNames = [...this.state.ruleNames];

    var ruleNames = await getRuleNames();
    this.setState({ ruleNames });

    // var removeRuleNames = lastRuleNames.map((x) => ruleNames.indexOf(x) !== -1);

    // if (removeRuleNames.length !== 0) {
    //   var ruleFilesDelta = { ...this.state.ruleFiles };
    //   var ruleInfosDelta = { ...this.state.ruleInfos };

    //   for (var removeRuleName of removeRuleNames) {
    //     ruleFilesDelta[removeRuleName] = null;
    //     ruleInfosDelta[removeRuleName] = null;
    //   }

    //   this.setState({
    //     ruleFiles: ruleFilesDelta,
    //     ruleInfos: ruleInfosDelta,
    //   });
    // }

    var newRuleNames = ruleNames.filter(
      (x) => this.state.ruleFiles[x] == null || this.state.ruleInfos[x] == null
    );

    for (var newRuleName of newRuleNames) {
      this.refreshRule(newRuleName);
    }
  }

  async refreshRule(ruleName) {
    if (ruleName == null) {
      return;
    }
    await this.refreshRuleInfo(ruleName);
    await this.refreshRuleFiles(ruleName);
  }

  async refreshRuleInfo(ruleName) {
    if (ruleName == null) {
      return;
    }
    var inject = await getRuleInfo(ruleName);
    this.setState((prev) => {
      var clone = Object.assign({}, prev.ruleInfos);
      clone[ruleName] = inject;
      return { ruleInfos: clone };
    });
  }

  async refreshRuleFiles(ruleName) {
    if (ruleName == null) {
      return;
    }
    var inject = await getRuleFiles(ruleName);
    this.setState((prev) => {
      var clone = Object.assign({}, prev.ruleFiles);
      clone[ruleName] = inject;
      return { ruleFiles: clone };
    });
  }

  getAppBinds() {
    return {
      setPage: this.setPage,
      refreshRuleNames: () => this.refreshRuleNames(),
      refreshRule: (x) => this.refreshRule(x),
      getRuleNames: () => this.state.ruleNames,
      getRuleInfo: (x) => this.state.ruleInfos[x],
      getRuleFiles: (x) => this.state.ruleFiles[x],
      viewRule: (x) => {
        this.setState({ ruleInspected: x });
        this.setPage("rule");
      },
    };
  }

  renderPage() {
    switch (this.state.page) {
      case "home":
        return <PageHome appBinds={this.getAppBinds()} />;
      case "search":
        return <PageSearch appBinds={this.getAppBinds()} />;
      case "rule":
        return (
          <PageRule
            appBinds={this.getAppBinds()}
            ruleName={this.state.ruleInspected}
          />
        );
      case "file":
        return <PageFile appBinds={this.getAppBinds()} />;
      default:
        return <PageNotFound appBinds={this.getAppBinds()} />;
    }
  }

  setPage = (newPage) => {
    if (newPage == null) {
      newPage = "home";
    }
    if (newPage !== this.state.page) {
      this.setState({
        page: newPage,
      });
    }
  };

  render() {
    return (
      <div className="App">
        <Navigation setPageFunc={this.setPage} />
        <section className="content">{this.renderPage()}</section>
      </div>
    );
  }
}

export default App;
