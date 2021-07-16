import React from "react";
import FileEmbed from "./fileEmbed";
import { getFileUrl } from "./apiHelper";

import "./pageFile.css";

class PageFile extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      metadata: null,
    };
  }

  componentDidMount() {
    this.downloadMetadata();
  }

  async downloadMetadata() {
    var metadata = await this.props.appBinds.getFileMetadata(this.props.fileID);
    this.setState({ metadata });
  }

  render() {
    var fileID = this.props.fileID;

    var metadata = this.state.metadata || {};
    var mime = metadata.mime || "?";

    var fileTitle = "File #" + fileID;

    var fullFileUrl = getFileUrl(fileID);

    return (
      <React.Fragment>
        <div className="full_file_sidebar">
          <h2>{fileTitle}</h2>
          <p>
            <a
              id="direct_download"
              href={fullFileUrl}
              target="_blank"
              rel="noreferrer"
            >
              Direct Download (<code>{mime + ""}</code>)
            </a>
          </p>

          <h3 id="actions_header">Actions</h3>
          <div id="actions_container"></div>
        </div>

        <FileEmbed
          appBinds={this.props.appBinds}
          fileID={this.props.fileID}
        ></FileEmbed>
      </React.Fragment>
    );
  }
}

export default PageFile;
