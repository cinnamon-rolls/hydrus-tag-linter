import React from "react";
import Thumbnail from "./thumbnail";

import "./gallery.css";
import AnchorButton from "./anchorButton";

class Gallery extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      filesCallback: this.props.filesCallback || (() => []),
      page: this.props.page || 1,
      filesPerPage: this.props.filesPerPage || 24,
      paginationButtons: this.props.paginationButtons || 3,
    };
  }

  setPage = (page) => {
    this.setState({ page });
  };

  setFilesPerPage = (filesPerPage) => {
    this.setState({ filesPerPage });
  };

  getFileIDs() {
    return this.state.filesCallback();
  }

  renderPaginationButton(currentPage, page, textOverride) {
    var text = textOverride || page + "";
    var key = "pagination-" + page + "-" + textOverride;
    if (currentPage === page) {
      return (
        <span key={key} className="pagination_entry">
          <b>{text}</b>
        </span>
      );
    } else {
      return (
        <AnchorButton
          key={key}
          onClick={() => this.setPage(page)}
          spanClassName="pagination_entry"
          buttonText={text}
        ></AnchorButton>
      );
    }
  }

  renderPagination(currentPage, firstPage, lastPage) {
    var buttons = [];

    if (currentPage !== firstPage) {
      buttons.push(this.renderPaginationButton(currentPage, firstPage, "<<"));
    }

    var padding = this.state.paginationButtons;
    var buttonsStart = Math.max(firstPage, currentPage - padding);
    var buttonsEnd = Math.min(lastPage + 1, currentPage + padding + 1);

    for (var i = buttonsStart; i < buttonsEnd; i++) {
      buttons.push(this.renderPaginationButton(currentPage, i));
    }

    if (currentPage !== lastPage && lastPage !== firstPage) {
      buttons.push(this.renderPaginationButton(currentPage, lastPage, ">>"));
    }

    return <div className="pagination">{buttons}</div>;
  }

  render() {
    var fileIDs = this.getFileIDs();

    if (fileIDs == null || fileIDs.length === 0) {
      return <p>Nobody home...</p>;
    }

    var page = this.state.page;
    var filesPerPage = this.state.filesPerPage;

    var firstPage = 1;
    var lastPage = Math.ceil(fileIDs.length / filesPerPage);

    var startIndex = (page - 1) * filesPerPage;
    var endIndex = page * filesPerPage;

    var fileIDsToRender = fileIDs.slice(
      startIndex,
      Math.min(fileIDs.length + 1, endIndex)
    );

    return (
      <div className="gallery_container">
        <div className="gallery">
          {fileIDsToRender.map((fileID) => (
            <Thumbnail
              key={"thumbnail-" + fileID}
              appBinds={this.props.appBinds}
              fileID={fileID}
            ></Thumbnail>
          ))}
        </div>
        {this.renderPagination(page, firstPage, lastPage)}
      </div>
    );
  }
}

export default Gallery;
