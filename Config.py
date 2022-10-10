import json

config_file = "config.json"


def get_from_dict(field_name, dict_field, json_field):
    if (field_name in dict_field.keys()) is False:
        return json_field.get(field_name).get("default")
    elif dict_field[field_name] is None:
        return json_field.get(field_name).get("default")
    else:
        return dict_field[field_name]


class ConfigYolov5Train():

    def __init__(self, config_dict):
        config = json.load(open(config_file))
        config = config.get("detail")
        config = config.get("train_config")
        self.ROOT = get_from_dict("ROOT", config_dict, config)
        self.weights = get_from_dict("weights", config_dict, config)
        self.cfg = get_from_dict("cfg", config_dict, config)
        self.data = get_from_dict("data", config_dict, config)
        self.hyp = get_from_dict("hyp", config_dict, config)
        self.epochs = get_from_dict("epochs", config_dict, config)
        self.batch_size = get_from_dict("batch-size", config_dict, config)
        self.imgsz = get_from_dict("imgsz", config_dict, config)
        self.rect = get_from_dict("rect", config_dict, config)
        self.resume = get_from_dict("resume", config_dict, config)
        self.nosave = get_from_dict("nosave", config_dict, config)
        self.noval = get_from_dict("noval", config_dict, config)
        self.noautoanchor = get_from_dict("noautoanchor", config_dict, config)
        self.evolve = get_from_dict("evolve", config_dict, config)
        self.bucket = get_from_dict("bucket", config_dict, config)
        self.cache = get_from_dict("cache", config_dict, config)
        self.image_weights = get_from_dict("image-weights", config_dict, config)
        self.device = get_from_dict("device", config_dict, config)
        self.multi_scale = get_from_dict("multi-scale", config_dict, config)
        self.single_cls = get_from_dict("single-cls", config_dict, config)
        self.optimizer = get_from_dict("optimizer", config_dict, config)
        self.sync_bn = get_from_dict("sync-bn", config_dict, config)
        self.workers = get_from_dict("workers", config_dict, config)
        self.project = get_from_dict("project", config_dict, config)
        self.name = get_from_dict("name", config_dict, config)
        self.exist_ok = get_from_dict("exist-ok", config_dict, config)
        self.quad = get_from_dict("quad", config_dict, config)
        self.linear_lr = get_from_dict("linear-lr", config_dict, config)
        self.label_smoothing = get_from_dict("label-smoothing", config_dict, config)
        self.patience = get_from_dict("patience", config_dict, config)
        self.freeze = get_from_dict("freeze", config_dict, config)
        self.save_period = get_from_dict("save-period", config_dict, config)
        self.local_rank = get_from_dict("local_rank", config_dict, config)
        self.entity = get_from_dict("entity", config_dict, config)
        self.upload_dataset = get_from_dict("upload_dataset", config_dict, config)
        self.bbox_interval = get_from_dict("bbox_interval", config_dict, config)
        self.artifact_alias = get_from_dict("artifact_alias", config_dict, config)


class ConfigYolov5Detect():

    def __init__(self, config_dict):
        config = json.load(open(config_file))
        config = config.get("detail")
        config = config.get("detect_config")
        self.ROOT = get_from_dict("ROOT", config_dict, config)
        self.weights = get_from_dict("weights", config_dict, config)
        self.source = get_from_dict("source", config_dict, config)
        self.data = get_from_dict("data", config_dict, config)
        self.imgsz = get_from_dict("imgsz", config_dict, config)
        self.conf_thres = get_from_dict("conf-thres", config_dict, config)
        self.iou_thres = get_from_dict("iou-thres", config_dict, config)
        self.max_det = get_from_dict("max-det", config_dict, config)
        self.device = get_from_dict("device", config_dict, config)
        self.view_img = get_from_dict("view-img", config_dict, config)
        self.save_txt = get_from_dict("save-txt", config_dict, config)
        self.save_conf = get_from_dict("save-conf", config_dict, config)
        self.save_crop = get_from_dict("save-crop", config_dict, config)
        self.nosave = get_from_dict("nosave", config_dict, config)
        self.classes = get_from_dict("classes", config_dict, config)
        self.agnostic_nms = get_from_dict("agnostic-nms", config_dict, config)
        self.augment = get_from_dict("augment", config_dict, config)
        self.visualize = get_from_dict("visualize", config_dict, config)
        self.update = get_from_dict("update", config_dict, config)
        self.project = get_from_dict("project", config_dict, config)
        self.name = get_from_dict("name", config_dict, config)
        self.exist_ok = get_from_dict("exist-ok", config_dict, config)
        self.line_thickness = get_from_dict("line-thickness", config_dict, config)
        self.hide_labels = get_from_dict("hide-labels", config_dict, config)
        self.hide_conf = get_from_dict("hide-conf", config_dict, config)
        self.half = get_from_dict("half", config_dict, config)
        self.dnn = get_from_dict("dnn", config_dict, config)


class ConfigYolov5Val():

    def __init__(self, config_dict):
        config = json.load(open(config_file))
        config = config.get("detail")
        config = config.get("val_config")
        #self.ROOT = config.get("ROOT").get("default")
        self.weights = get_from_dict("weights", config_dict, config)
        self.data = get_from_dict("data", config_dict, config)
        self.batch_size = get_from_dict("batch-size", config_dict, config)
        self.imgsz = get_from_dict("imgsz", config_dict, config)
        self.workers = get_from_dict("workers", config_dict, config)
        self.conf_thres = get_from_dict("conf-thres", config_dict, config)
        self.iou_thres = get_from_dict("iou-thres", config_dict, config)
        self.task = get_from_dict("task", config_dict, config)
        self.device = get_from_dict("device", config_dict, config)
        self.save_txt = get_from_dict("save-txt", config_dict, config)
        self.save_conf = get_from_dict("save-conf", config_dict, config)
        self.save_hybrid = get_from_dict("save-hybrid", config_dict, config)
        self.save_json = get_from_dict("save-json", config_dict, config)
        self.single_cls = get_from_dict("single-cls", config_dict, config)
        self.augment = get_from_dict("augment", config_dict, config)
        self.verbose = get_from_dict("verbose", config_dict, config)
        self.project = get_from_dict("project", config_dict, config)
        self.name = get_from_dict("name", config_dict, config)
        self.exist_ok = get_from_dict("exist-ok", config_dict, config)
        self.half = get_from_dict("half", config_dict, config)
        self.dnn = get_from_dict("dnn", config_dict, config)

class ConfigYolov5Compare():

    def __init__(self, config_dict):
        config = json.load(open(config_file))
        config = config.get("detail")
        config = config.get("compare_config")
        #self.ROOT = config.get("ROOT").get("default")
        self.weights_compare = get_from_dict("weights_compare", config_dict, config)
        self.weights_best_model = get_from_dict("weights_best_model", config_dict, config)
        self.data = get_from_dict("data", config_dict, config)
        self.batch_size = get_from_dict("batch-size", config_dict, config)
        self.imgsz = get_from_dict("imgsz", config_dict, config)
        self.workers = get_from_dict("workers", config_dict, config)
        self.conf_thres = get_from_dict("conf-thres", config_dict, config)
        self.iou_thres = get_from_dict("iou-thres", config_dict, config)
        self.task = get_from_dict("task", config_dict, config)
        self.device = get_from_dict("device", config_dict, config)
        self.save_txt = get_from_dict("save-txt", config_dict, config)
        self.save_conf = get_from_dict("save-conf", config_dict, config)
        self.save_hybrid = get_from_dict("save-hybrid", config_dict, config)
        self.save_json = get_from_dict("save-json", config_dict, config)
        self.single_cls = get_from_dict("single-cls", config_dict, config)
        self.augment = get_from_dict("augment", config_dict, config)
        self.verbose = get_from_dict("verbose", config_dict, config)
        self.project = get_from_dict("project", config_dict, config)
        self.name = get_from_dict("name", config_dict, config)
        self.exist_ok = get_from_dict("exist-ok", config_dict, config)
        self.half = get_from_dict("half", config_dict, config)
        self.dnn = get_from_dict("dnn", config_dict, config)

if __name__ == '__main__':
    dict = {
        "ROOT": "ABC",
        "weights": "runs/1/1/last.pt",
    }
    train_config = ConfigYolov5Train(dict)
    print(train_config.weights, train_config.ROOT, train_config.data)



