// import "./App.css";
import React from "react";
import Navigation from "./components/navigation";

import PageHome from "./components/pageHome";
import PageSearch from "./components/pageSearch";
import PageNotFound from "./components/pageNotFound";

class App extends React.Component {
  state = {
    page: "home",
  };

  renderPage() {
    switch (this.state.page) {
      case "home":
        return <PageHome />;
      case "search":
        return <PageSearch />;
      default:
        return <PageNotFound />;
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
