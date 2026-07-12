// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['kaitai-struct/KaitaiStream'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('kaitai-struct/KaitaiStream'));
  } else {
    root.Th14 = factory(root.KaitaiStream);
  }
}(typeof self !== 'undefined' ? self : this, function (KaitaiStream) {
var Th14 = (function() {
  function Th14(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  Th14.prototype._read = function() {
    this.header = new Header(this._io, this, this._root);
    this.stages = [];
    for (var i = 0; i < this.header.stageCount; i++) {
      this.stages.push(new Stage(this._io, this, this._root));
    }
  }

  var Header = Th14.Header = (function() {
    function Header(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Header.prototype._read = function() {
      this.name = KaitaiStream.bytesToStr(KaitaiStream.bytesTerminate(this._io.readBytes(12), 0, false), "SJIS");
      this.timestamp = this._io.readU8le();
      this.score = this._io.readU4le();
      this.unknown1 = this._io.readBytes(92);
      this.slowdown = this._io.readF4le();
      this.stageCount = this._io.readU4le();
      this.shot = this._io.readU4le();
      this.subshot = this._io.readU4le();
      this.difficulty = this._io.readU4le();
      this.cleared = this._io.readU4le();
      this.unknown2 = this._io.readU4le();
      this.spellPracticeId = this._io.readU4le();
    }

    return Header;
  })();

  var Stage = Th14.Stage = (function() {
    function Stage(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Stage.prototype._read = function() {
      this.stageNum = this._io.readU2le();
      this.rng = this._io.readU2le();
      this.frameCount = this._io.readU4le();
      this.endOff = this._io.readU4le();
      this.posSubpixelX = this._io.readU4le();
      this.posSubpixelY = this._io.readU4le();
      this.shot = this._io.readU4le();
      this.subshot = this._io.readU4le();
      this.score = this._io.readU4le();
      this.difficulty = this._io.readU4le();
      this.continues = this._io.readU4le();
      this.unknown1 = this._io.readU4le();
      this.graze = this._io.readU4le();
      this.spellPracticeId = this._io.readU4le();
      this.unknown2 = this._io.readU4le();
      this.piv = this._io.readU4le();
      this.pivMin = this._io.readU4le();
      this.pivMax = this._io.readU4le();
      this.power = this._io.readU4le();
      this.powerMax = this._io.readU4le();
      this.powerLevelUp = this._io.readU4le();
      this.lives = this._io.readU4le();
      this.lifePieces = this._io.readU4le();
      this.unknown3 = this._io.readU4le();
      this.bombs = this._io.readU4le();
      this.bombPieces = this._io.readU4le();
      this.scoreFromPoc = this._io.readU4le();
      this.unknown4 = this._io.readU4le();
      this.unknown5 = this._io.readU4le();
      this.unknown6 = this._io.readU4le();
      this.lastItemCollectedPos = [];
      for (var i = 0; i < 3; i++) {
        this.lastItemCollectedPos.push(this._io.readF4le());
      }
      this.pocCount = this._io.readU4le();
      this.focused = this._io.readU4le();
      this.spellCardRealTimes = [];
      for (var i = 0; i < 21; i++) {
        this.spellCardRealTimes.push(this._io.readU4le());
      }
      this.stageData = this._io.readBytes(this.endOff);
    }

    return Stage;
  })();

  return Th14;
})();
return Th14;
}));
