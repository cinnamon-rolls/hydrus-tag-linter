import React from "react";
import FileEmbed from "./fileEmbed";

import "./pageFile.css";

class PageFile extends React.Component {
  render() {
    return (
      <React.Fragment>
        <FileEmbed
          appBinds={this.props.appBinds}
          fileID={this.props.fileID}
        ></FileEmbed>
      </React.Fragment>
    );
  }
}

export default PageFile;
