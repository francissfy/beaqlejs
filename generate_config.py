import os
import json
import argparse
from typing import List, Dict, Union


def get_test_cases(audio_path: str, cate1: str, cate2: str) -> List[Dict[str, Union[str, Dict]]]:
    cates = [p for p in os.listdir(audio_path) if p[0] != "."]
    assert cate1 in cates
    assert cate2 in cates
    files = {}
    cates = [cate1, cate2]
    for c in cates:
        path = os.path.join(audio_path, c)
        c_files = [f for f in os.listdir(path) if f[0] != "."]
        files[c] = [os.path.join(path, f) for f in c_files]
    c1_files = files[cate1]
    c2_files = files[cate2]
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
    return test_cases

def gen_config_html(cate1: str, cate2: str, audio_path: str, num_per_run: int = 10, base_html_file: str = "index_template.html"):
    test_cases = get_test_cases(audio_path, cate1, cate2)
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
	    "MaxTestsPerRun": num_per_run,
        "CateMapping": {"A": cate1, "B": cate2},
        "Testsets": test_cases
    }
    config_name = f"{cate1}_vs_{cate2}.js"
    with open(f"./config/{config_name}", "w") as wf:
        wf.write("var TestConfig = ")
        wf.write(json.dumps(config_dict, indent=4))
    html_base = open(base_html_file, "r").read()
    config_name = f"{cate1}_vs_{cate2}.js"
    assert "config/configuration.js" in html_base
    html_base = html_base.replace("config/configuration.js", f"config/{config_name}")
    html_name = f"{cate1}_vs_{cate2}.html"
    with open(html_name, "w") as wf:
        wf.write(html_base)
    print(f"Generate config: {config_name}, html: {html_name}")
    

def main(args: argparse.Namespace):
    base_cate = args.base_cate
    cmp_cates = args.cmp_cates
    for cmpc in cmp_cates:
        gen_config_html(base_cate, cmpc, args.audio_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-path", type=str, default="./audio/melgan")
    parser.add_argument("--base-cate", type=str, default="trans_conv_oov50_top10")
    parser.add_argument("--cmp-cates", type=str, nargs="+", default=["tts3_top10", "tts3_bert_top10", "tts3_glove_top10"])
    args = parser.parse_args()
    main(args)
