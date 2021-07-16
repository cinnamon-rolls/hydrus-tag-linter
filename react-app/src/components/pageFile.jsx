import React from "react";
import FileEmbed from "./fileEmbed";
import FileTags from "./fileTags";
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

          <h3>Actions</h3>
          <div>{/* actions go here */}</div>

          <h3>Tags</h3>
          <FileTags metadata={metadata} />
        </div>

        <FileEmbed appBinds={this.props.appBinds} fileID={this.props.fileID} />
      </React.Fragment>
    );
  }
}

export default PageFile;
