import React from "react";
import { getFileUrl } from "./apiHelper";
import Loading from "./loading";
import Thumbnail from "./thumbnail";

class FileEmbed extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      metadata: null,
    };
  }

  async fetchMetadata() {
    var appBinds = this.props.appBinds;
    var metadata = await appBinds.getFileMetadata(this.props.fileID);
    this.setState({ metadata });
  }

  componentDidMount() {
    this.fetchMetadata();
  }

  render() {
    var fileID = this.props.fileID;
    if (fileID == null) {
      return <span>ERROR: no fileID</span>;
    }

    return (
      <div className="full_file_container">{this.renderAsSomething()}</div>
    );
  }

  renderAsSomething() {
    var metadata = this.state.metadata;
    if (metadata == null) {
      return <Loading />;
    }

    var fileID = this.props.fileID;
    var mime = metadata.mime;

    if (mime.startsWith("image")) {
      return this.renderAsImage(fileID);
    } else if (mime.startsWith("audio")) {
      return this.renderAsAudio(fileID, mime);
    } else if (mime.startsWith("video")) {
      return this.renderAsVideo(fileID, mime);
    } else {
      return this.renderAsUnknown(fileID, mime);
    }
  }

  renderAsImage(fileID) {
    return (
      <img
        className="full_file"
        src={getFileUrl(fileID)}
        alt={"Full file #" + fileID}
      />
    );
  }

  renderSourceElement(fileID, mime) {
    return (
      <source className="full_file" src={getFileUrl(fileID)} type={mime} />
    );
  }

  renderAsAudio(fileID, mime) {
    return (
      <audio className="full_file" controls>
        {this.renderSourceElement(fileID, mime)}
      </audio>
    );
  }

  renderAsVideo(fileID, mime) {
    return (
      <video className="full_file" controls>
        {this.renderSourceElement(fileID, mime)}
      </video>
    );
  }

  renderAsUnknown(fileID, mime) {
    return (
      <div>
        <span>
          I am not sure how to render <code>{mime}</code> types.
        </span>
        <br />
        <Thumbnail fileID={fileID}></Thumbnail>
      </div>
    );
  }
}

export default FileEmbed;
