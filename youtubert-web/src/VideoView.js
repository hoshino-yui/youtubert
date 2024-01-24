import React, {useState} from "react";
import "./VideoView.css"
import {Link} from "react-aria-components";

const timeMarkRegexString = "\\d+:\\d+(?::\\d+)?";

function parseTimeMark(timeMarkString) {
  // [second, minute, hour(optional)]
  const timeMarkComponents = timeMarkString
    .split(':')
    .reverse()
    .map(timeMarkComponentString => parseInt(timeMarkComponentString));

  let seconds = 0;
  timeMarkComponents.forEach((component, index) => seconds += component * Math.pow(60, index));
  return seconds
}

function makeTimeMarkClickable(text, setTimeMark) {

  const parts = text.split(new RegExp(`(${timeMarkRegexString})`, 'g'));
  return (<span> {
    parts.map(part => {
        if (part.match(`^${timeMarkRegexString}$`)) {
          return <Link onPress={e => {
              setTimeMark(parseTimeMark(part))
            }}>{part}</Link>;
        } else {
          return <span>{part}</span>;
        }
      }
    )
  } </span>);
}

function highlightText(text, searchText, setTimeMark) {
  const parts = searchText ? text.split(new RegExp(`(${searchText})`, 'gi')) : [text];
  return (<span> {
    parts.map(part =>
      part.toLowerCase() === searchText?.toLowerCase()
        ? <span className="search-text">{part}</span>
        : <span>{makeTimeMarkClickable(part, setTimeMark)}</span>
    )
  } </span>);
}

function VideoView({video, searchText}) {
  const [timeMark, setTimeMark] = useState(0);
  const [timeMarkKey, setTimeMarkKey] = useState(0);
  const setTimeMarkAndKey = e => {
    setTimeMark(e);
    setTimeMarkKey(timeMarkKey + 1);
  }
  return (video &&
    <div className="video-view">
      <div style={{textAlign: "center"}}>
        <iframe title="youtube"
                src={`https://www.youtube.com/embed/${video.video_id}?autoplay=${timeMark ? 1 : 0}&amp;start=${timeMark}`}
                frameBorder="0"
                allow={"autoplay; picture-in-picture; web-share"}
                key={timeMarkKey}
                allowFullScreen/>
      </div>
      <div>
        <p>{video.timestamp}</p>
        <h3><a href={video.webpage_url} target="_blank" rel="noopener noreferrer">{video.title}</a></h3>
        <p><a href={`https://youtube.com/channel/${video.channel_id}`} target="_blank"
              rel="noopener noreferrer">{video.channel}</a>
        </p>
        {video.comments.map(comment =>
          <p className="comment" id={comment.id}>
            {comment.text.split('\n').map(line => (<span>{highlightText(line, searchText, setTimeMarkAndKey)}<br/></span>))}
          </p>
        )}
      </div>

    </div>
  )
}

export default VideoView;
