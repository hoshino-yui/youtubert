import './App.css';
import suzuka from './data/鈴花ステラ Ch.  Suzuka Stella - UChAOCCFuF2hto05Z68xp56A'
import luna from './data/望月ルーナ  Mochitsugi Luna Ch. - UCKiWJEjJw-zGW_Co_kJt5dw'
import cross from './data/Cross Ch. 月島クロス【HKVTuber】 - UC5bhpsL8ZUHQ9q-HOLVc82A'
import kurona from './data/Kurona Ch.酒吞玖蘿娜【innoneer.TV】 - UCYPr6jNySMcfpjheFi61U8w.json'
import tama from './data/QuonTama Ch. 久遠たま - UCBC7vYFNQoGPupe5NxPG4Bw'
import rumii from './data/Rumii Ch. 如月ルミィ【HKVTuber】 - UCJcKh9mwJH4zhHsU4NDs54g'
import aisu from './data/小林冰 Aisu Ch.  - UCnwgM2M3C4JOVdOZ0OLu_bA.json'
import saki from './data/瑠凜紗紀-RuriSaki【HKVtuber】 - UCwwvI-bV0CQ4FwkF-Kg0NBQ'

import React, {useState} from "react";
import {SearchField, Label, Input, Button} from 'react-aria-components';
import VideoSelector from "./VideoSelector";
import VideoView from "./VideoView";
import ChannelSelector from "./ChannelSelector";


function getVideos() {
  const videos = new Map();
  [suzuka, luna, cross, kurona, tama, rumii, aisu, saki]
    .flatMap(c => c)
    .forEach(v => videos.set(v.video_id, v));
  return videos;
}

function getChannels(videos) {
  const channels = new Map();
  videos.forEach(v => channels.set(v.channel_id, v.channel));
  return channels;
}

function App() {
  const videosMap = getVideos();
  const channels = getChannels(Array.from(videosMap.values()));
  const [searchText, setSearchText] = useState();
  const [selectedChannel, setSelectedChannel] = useState(new Set([Array.from(channels.keys())[0]]));
  const [selectedVideos, setSelectedVideos] = useState(new Set());
  const theSearchText = searchText ?.trim();


  let videosList = Array.from(videosMap.values());
  videosList = videosList.filter(v => Array.from(selectedChannel).includes(v.channel_id));
  if (theSearchText) {
    videosList = videosList.filter(v => v.comments.flatMap(c => c.text.toLowerCase()).join().includes(theSearchText.toLowerCase()));
  }
  const theVideo = videosMap.get(selectedVideos.values().next().value);
  return (
    <div style={{margin: "10px"}}>
      <div style={{margin: "5px"}}>
        <div style={{display: "flex", justifyContent: "center"}}>
          <SearchField onChange={setSearchText} onClear={() => setSearchText('')}>
            <Label>Search</Label>
            <Input/>
            <Button>✕</Button>
          </SearchField>
        </div>
        <ChannelSelector channels={channels} selectedChannel={selectedChannel} setSelectedChannel={setSelectedChannel}/>

      </div>
      <div style={{display: 'flex'}}>
        <VideoSelector videos={videosList} selectedVideos={selectedVideos} handleSelectVideo={setSelectedVideos}/>
        <VideoView video={theVideo} searchText={theSearchText}/>
      </div>

      <div>
        searchText = {theSearchText}<br/>
        selectedVideos = {selectedVideos}<br/>
        selectedChannel = {Array.from(selectedChannel).join(', ')}<br/>
      </div>

    </div>

  );
}

export default App;
