import React from "react";
import Thumbnail from "./thumbnail";

class Gallery extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      filesCallback: this.props.filesCallback || (() => []),
    };
  }

  getFileIDs() {
    return this.state.filesCallback();
  }

  render() {
    var fileIDs = this.getFileIDs();

    if (fileIDs.length === 0) {
      return <p>Nobody home...</p>;
    }

    return (
      <div className="gallery">
        {fileIDs.map((fileID) => (
          <Thumbnail
            key={"thumbnail-" + fileID}
            appBinds={this.props.appBinds}
            fileID={fileID}
          ></Thumbnail>
        ))}
      </div>
    );
  }
}

export default Gallery;
