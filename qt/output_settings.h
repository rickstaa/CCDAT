#ifndef OUTPUT_SETTINGS_H
#define OUTPUT_SETTINGS_H

#include <QDialog>

namespace Ui {
class output_settings;
}

class output_settings : public QDialog
{
    Q_OBJECT

public:
    explicit output_settings(QWidget *parent = nullptr);
    ~output_settings();

private:
    Ui::output_settings *ui;
};

#endif // OUTPUT_SETTINGS_H
