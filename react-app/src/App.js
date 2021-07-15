// import logo from "./logo.svg";
// import "./App.css";
import React from "react";
import Navigation from "./components/navigation";

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <Navigation />
        <section class="content">
          <p>Hello World</p>
        </section>
      </div>
    );
  }
}

export default App;
