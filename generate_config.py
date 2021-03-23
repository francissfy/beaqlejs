import os
import json
import argparse


def main(args: argparse.Namespace):
    audio_path = args.audio_dir
    cates = [p for p in os.listdir(audio_path) if p[0] != "."]
    for c in args.cates:
        assert c in cates, f"{c} not found"
    cates = args.cates
    assert len(cates) == 2, "AB test only support two categories"
    files = {}
    for c in cates:
        path = os.path.join(audio_path, c)
        c_files = [f for f in os.listdir(path) if f[0] != "."]
        files[c] = [os.path.join(path, f) for f in c_files][args.offset: args.end]
    c1, c2 = files.keys()
    c1_files = files[c1]
    c2_files = files[c2]
    assert len(c1_files) == len(c2_files), ""
    ids = list(range(len(c1_files)))
    test_cases = [
        {
            "Name": str(uid),
            "TestID": str(uid),
            "Files": {
                "A": f1,
                "B": f2,
            }
        } for uid, f1, f2 in zip(ids, c1_files, c2_files)
    ]
    config_dict = {
        "TestName": "IS2021",
        "LoopByDefault": True,
        "ShowFileIDs": False,
        "ShowResults": True,
        "EnableABLoop": True,
        "EnableOnlineSubmission": False,
        "BeaqleServiceURL": "/web_service/beaqleJS_Service.php",
        "SupervisorContact": "",
        "AudioRoot": "",
        "RandomizeFileOrder": True,
        "CateMapping": {"A": c1, "B": c2},
        "Testsets": test_cases
    }

    with open(args.config_file, "w") as wf:
        # wf.write(f"// A: {c1} B: {c2} \n")
        wf.write("var TestConfig = ")
        wf.write(json.dumps(config_dict, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-dir", type=str, default="./audio")
    parser.add_argument("--cates", type=str, nargs="+", default=[])
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--config-file", type=str, default="./config/config/pref_test.js")
    args = parser.parse_args()
    main(args)
