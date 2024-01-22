import React from "react";
import "./VideoView.css"

function highlightText(text, searchText) {
  if (searchText) {
    const parts = text.split(new RegExp(`(${searchText})`, 'gi'));
    return (<span> {
      parts.map(part =>
        part.toLowerCase() === searchText.toLowerCase()
          ? <span className="search-text">{part}</span>
          : <span>{part}</span>
      )
    } </span>);
  } else {
    return text;
  }
}

function VideoView({video, searchText}) {
  return (video &&
    <div className="video-view">
      <div style={{textAlign: "center"}}>
        <iframe title="youtube" src={`https://www.youtube.com/embed/${video.video_id}`} allowFullScreen/>
      </div>
      <div>
        <p>{video.timestamp}</p>
        <h3><a href={video.webpage_url} target="_blank" rel="noopener noreferrer">{video.title}</a></h3>
        <p><a href={`https://youtube.com/channel/${video.channel_id}`} target="_blank"
              rel="noopener noreferrer">{video.channel}</a>
        </p>
        {video.comments.map(comment =>
          <p className="comment" id={comment.id}>
            {comment.text.split('\n').map(line => (<span>{highlightText(line, searchText)}<br/></span>))}
          </p>
        )}
      </div>

    </div>
  )
}

export default VideoView;
