#!/usr/bin/env python3
import os, json, argparse, requests, datetime
from jinja2 import Environment, FileSystemLoader

def get_api(url, user=None, token=None, path="/api/json"):
    auth = (user, token) if user and token else None
    r = requests.get(url.rstrip('/') + path, auth=auth, timeout=10)
    r.raise_for_status()
    return r.json()

def plugin_list(url, user=None, token=None):
    """
    Return a tuple (plugins_list, error_message_or_none).
    Plugins_list is always a list (possibly empty).
    """
    try:
        r = get_api(url, user, token, "/pluginManager/api/json?depth=1")
        plugins = r.get("plugins", [])
        plugins_list = [{"shortName": p.get("shortName"), "version": p.get("version"), "enabled": p.get("enabled")} for p in plugins]
        return plugins_list, None
    except Exception as e:
        return [], str(e)

def basic_metrics(url, user=None, token=None):
    out = {}
    try:
        api = get_api(url, user, token)
        out['version'] = api.get('version')
        out['numExecutors'] = api.get('numExecutors')
        out['jobs'] = [{"name": j.get("name")} for j in api.get('jobs',[])]
    except Exception as e:
        out['error'] = str(e)
    return out

def render_html(report, outpath):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
    tpl = env.get_template("report_template.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(tpl.render(report=report, generated=str(datetime.datetime.utcnow())))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default=os.environ.get('JENKINS_URL','http://localhost:8080'))
    parser.add_argument('--user', default=os.environ.get('JENKINS_USER'))
    parser.add_argument('--token', default=os.environ.get('JENKINS_TOKEN'))
    parser.add_argument('--output', default='report.json')
    parser.add_argument('--render', default=None)
    args = parser.parse_args()

    report = {}
    report['target'] = args.url
    report['basic'] = basic_metrics(args.url, args.user, args.token)

    plugins, plugin_error = plugin_list(args.url, args.user, args.token)
    report['plugins'] = plugins
    if plugin_error:
        report['plugin_error'] = plugin_error

    # (you can add more checks here and add them to report)

    # ensure output directory exists when running inside a container with mount
    output_path = args.output
    outdir = os.path.dirname(output_path)
    if outdir and not os.path.exists(outdir):
        try:
            os.makedirs(outdir, exist_ok=True)
        except Exception:
            pass

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if args.render:
        try:
            render_html(report, args.render)
        except Exception as e:
            # if rendering fails, still keep the JSON report and show error
            print("Rendering error:", e)
            # optionally write a minimal HTML fallback
            fallback = {"error": str(e)}
            with open(args.render, "w", encoding="utf-8") as f:
                f.write("<html><body><h1>Rendering failed</h1><pre>{}</pre></body></html>".format(str(e)))

if __name__ == '__main__':
    main()
