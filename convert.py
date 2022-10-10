
import yaml
import glob
import os


def convert_yolo_format_data(labels_folder="label", new_labels_folder="new_label", folder=None):
    classes = []
    if not os.path.exists(new_labels_folder):
        os.mkdir(new_labels_folder)
    for file in glob.glob(labels_folder+"/*.txt"):
        label_file = open(file, "r")
        new_label_file = open(new_labels_folder+file[len(labels_folder):], "w")
        labels = label_file.readlines()
        for label in labels:
            obj = label.split(" ")
            if not (obj[0] in classes):
                classes.append(obj[0])
            index = classes.index(obj[0])
            try:
                new_label_file.write(f'{index} {float(obj[1])+float(obj[3])/2} {float(obj[2])+float(obj[4])/2} {float(obj[3])} {float(obj[4])}')
            except ValueError:
                print("value error")
            except IndexError:
                print("index error")
            
    data = dict(
        train=folder+'/training/images',
        val=folder+'/validation/images',
        test=folder+"/testing/images",
        nc=len(classes),
        names=classes
    )
    with open(f'{folder}/data.yaml', 'w') as outfile:
        yaml.safe_dump(data, outfile, default_flow_style=False)
