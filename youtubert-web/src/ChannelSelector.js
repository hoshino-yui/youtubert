import React from "react";
import "./ChannelSelector.css"
import {Button, Label, Tag, TagGroup, TagList} from "react-aria-components";

function ChannelSelector({channels, selectedChannel, setSelectedChannel}) {
  return <TagGroup selectionMode="multiple" selectedKeys={selectedChannel} onSelectionChange={setSelectedChannel}>
    <Label>Channels</Label>
    <div>
      <Button className="positive" onPress={() => setSelectedChannel(new Set(channels.keys()))}>Select All</Button>
      <Button className="negative" onPress={() => setSelectedChannel(new Set())}>Deselect All</Button>
    </div>
    <TagList>
      {Array.from(channels).map(([c_id, c_name]) => <Tag id={c_id}>{c_name}</Tag>)}
    </TagList>
  </TagGroup>
}

export default ChannelSelector;
